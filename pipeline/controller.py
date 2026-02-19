from PySide6.QtCore import QThread, Signal
from pipeline.ollama_client import stream_generate


# --- Single mode prompts (3-stage collaborative) ---

SINGLE_REASONING_PROMPT = """\
You are a reasoning model. Analyze the question and provide your best \
initial answer with step-by-step reasoning.
{context}
Question:
{question}

Provide a thorough initial analysis:
"""

SINGLE_JUDGE_PROMPT = """\
You are a knowledgeable judge model. You have received an initial analysis \
from another model. Your job is NOT just to find flaws — you must actively \
complement and enrich the answer with your own knowledge, additional \
perspectives, missing details, and deeper insights.
{context}
Original question:
{question}

Initial analysis:
{reasoning_output}

Complement this answer: add what was missed, expand on key points, \
correct any errors, and contribute your own knowledge:
"""

SINGLE_FINAL_PROMPT = """\
You are the final synthesis model. You have the original reasoning and \
the judge's complementary analysis. Synthesize both into one clear, \
complete, and well-structured final answer. Respond in the same language \
as the original question.
{context}
Original question:
{question}

Initial reasoning:
{reasoning_output}

Judge's complement:
{judge_output}

Produce the final consolidated answer:
"""

# --- Debate mode prompts ---

DEBATE_ROUND1_PROMPT = """\
You are participating in a structured debate. Analyze the question and present \
your initial position with clear, step-by-step reasoning.
{context}
Question:
{question}

Present your initial position and reasoning:
"""

DEBATE_ROUND2_PROMPT = """\
You are in round 2 of a structured debate. You have seen the other participants' \
initial positions. Respond to their arguments: address their specific points, \
challenge weaknesses in their reasoning, and defend or refine your own position.
{context}
Question:
{question}

Other participants' initial positions:
{other_responses}

Your initial position was:
{own_response}

Respond to the other arguments and defend/refine your position:
"""

DEBATE_CLOSING_PROMPT = """\
You are delivering your final closing statement in a structured debate. \
Review all arguments made across both rounds and give a concise, \
well-reasoned closing statement of your position.
{context}
Question:
{question}

Full debate so far:
{debate_history}

Your closing statement:
"""

DEBATE_JUDGE_PROMPT = """\
You are a critical evaluator reviewing a structured multi-round debate.
{context}
Original question:
{question}

Full debate (Round 1, Round 2, and Closing Statements):
{responses}

Tasks:
1. Evaluate the quality of reasoning across all rounds
2. Identify who made the strongest arguments and why
3. Identify logical flaws or missing considerations
4. Determine which position is best supported by the evidence
5. Explain your decision clearly
"""

DEBATE_FINAL_PROMPT = """\
Respond in the same language as the original question.
{context}
Original question:
{question}

Full debate:
{responses}

Judge decision:
{judge_output}

Based on the judge's evaluation, produce a clear, direct, \
and consolidated final answer to the original question.
"""


class PipelineThread(QThread):
    token_update = Signal(str)
    final_token = Signal(str)
    stage_complete = Signal(str, str)
    finished_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self._stopped = False

    def stop(self):
        self._stopped = True

    def _is_stopped(self):
        return self._stopped

    def _stream(self, model, prompt, temperature=0.7, is_final=False):
        def on_token(t):
            self.token_update.emit(t)
            if is_final:
                self.final_token.emit(t)

        return stream_generate(
            model,
            prompt,
            port=self.config["port"],
            temperature=temperature,
            callback=on_token,
            cancel_check=self._is_stopped,
        )

    def run(self):
        try:
            if self.config["mode"] == "single":
                self._run_single()
            else:
                self._run_debate()
        except Exception as e:
            if not self._stopped:
                self.error_signal.emit(str(e))

    def _get_context_block(self):
        parts = []
        file_ctx = self.config.get("file_context", "")
        if file_ctx:
            parts.append(f"\nAttached file:\n{file_ctx}\n")
        chat_ctx = self.config.get("chat_context", "")
        if chat_ctx:
            parts.append(f"\nConversation so far:\n{chat_ctx}\n")
        return "".join(parts)

    # --- Single mode: Reasoning -> Judge complements -> Final synthesizes ---

    def _run_single(self):
        cfg = self.config
        context = self._get_context_block()

        # Stage 1: Reasoning — initial idea
        self.token_update.emit(f"\n=== Reasoning: {cfg['reasoning_model']} ===\n\n")
        reasoning_prompt = SINGLE_REASONING_PROMPT.format(
            question=cfg["question"], context=context
        )
        reasoning_output = self._stream(cfg["reasoning_model"], reasoning_prompt)
        if self._stopped:
            return
        self.stage_complete.emit("reasoning", reasoning_output)

        # Stage 2: Judge — complements with own knowledge
        self.token_update.emit(f"\n\n=== Judge: {cfg['judge_model']} ===\n\n")
        judge_prompt = SINGLE_JUDGE_PROMPT.format(
            question=cfg["question"],
            reasoning_output=reasoning_output,
            context=context,
        )
        judge_output = self._stream(cfg["judge_model"], judge_prompt, temperature=0.4)
        if self._stopped:
            return
        self.stage_complete.emit("judge", judge_output)

        # Stage 3: Final — synthesizes both into clean answer
        self.token_update.emit(f"\n\n=== Final: {cfg['final_model']} ===\n\n")
        final_prompt = SINGLE_FINAL_PROMPT.format(
            question=cfg["question"],
            reasoning_output=reasoning_output,
            judge_output=judge_output,
            context=context,
        )
        final_answer = self._stream(cfg["final_model"], final_prompt, temperature=0.5, is_final=True)
        if self._stopped:
            return
        self.stage_complete.emit("final", final_answer)
        self.finished_signal.emit(final_answer)

    # --- Debate mode: Round 1 -> Round 2 -> Closing -> Judge -> Final ---

    def _run_debate(self):
        cfg = self.config
        context = self._get_context_block()
        models = cfg["debate_models"]

        # Round 1: each model states its initial position
        round1 = {}
        for model in models:
            if self._stopped:
                return
            self.token_update.emit(f"\n=== Round 1 — {model} ===\n\n")
            answer = self._stream(model, DEBATE_ROUND1_PROMPT.format(
                question=cfg["question"], context=context
            ))
            if self._stopped:
                return
            round1[model] = answer
            self.stage_complete.emit(f"debate_r1:{model}", answer)

        # Round 2: each model reads the others' R1 and responds
        round2 = {}
        for model in models:
            if self._stopped:
                return
            others = "\n\n".join(
                f"{m}:\n{r}" for m, r in round1.items() if m != model
            )
            self.token_update.emit(f"\n\n=== Round 2 — {model} ===\n\n")
            answer = self._stream(model, DEBATE_ROUND2_PROMPT.format(
                question=cfg["question"],
                context=context,
                other_responses=others,
                own_response=round1[model],
            ))
            if self._stopped:
                return
            round2[model] = answer
            self.stage_complete.emit(f"debate_r2:{model}", answer)

        # Closing statements: each model sees full R1 + R2 exchange
        history_parts = []
        for m in models:
            history_parts.append(f"Round 1 — {m}:\n{round1[m]}")
        for m in models:
            history_parts.append(f"Round 2 — {m}:\n{round2[m]}")
        debate_history = "\n\n".join(history_parts)

        closing = {}
        for model in models:
            if self._stopped:
                return
            self.token_update.emit(f"\n\n=== Closing — {model} ===\n\n")
            answer = self._stream(model, DEBATE_CLOSING_PROMPT.format(
                question=cfg["question"],
                context=context,
                debate_history=debate_history,
            ))
            if self._stopped:
                return
            closing[model] = answer
            self.stage_complete.emit(f"debate_closing:{model}", answer)

        # Build the full debate transcript for judge and final
        closing_parts = "\n\n".join(f"Closing — {m}:\n{s}" for m, s in closing.items())
        full_debate = debate_history + "\n\n" + closing_parts

        # Judge evaluates the complete debate
        self.token_update.emit(f"\n\n=== Judge: {cfg['judge_model']} ===\n\n")
        judge_prompt = DEBATE_JUDGE_PROMPT.format(
            question=cfg["question"], responses=full_debate, context=context
        )
        judge_output = self._stream(cfg["judge_model"], judge_prompt, temperature=0.3)
        if self._stopped:
            return
        self.stage_complete.emit("judge", judge_output)

        # Final synthesizes
        self.token_update.emit(f"\n\n=== Final: {cfg['final_model']} ===\n\n")
        final_prompt = DEBATE_FINAL_PROMPT.format(
            question=cfg["question"],
            responses=full_debate,
            judge_output=judge_output,
            context=context,
        )
        final_answer = self._stream(cfg["final_model"], final_prompt, temperature=0.5, is_final=True)
        if self._stopped:
            return
        self.stage_complete.emit("final", final_answer)
        self.finished_signal.emit(final_answer)
