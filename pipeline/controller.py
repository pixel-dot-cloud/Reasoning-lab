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

DEBATE_PROMPT = """\
Analyze the following question carefully and provide structured reasoning \
followed by a clear conclusion.
{context}
Question:
{question}
"""

DEBATE_JUDGE_PROMPT = """\
You are a critical evaluator.
{context}
Original question:
{question}

Model responses:
{responses}

Tasks:
1. Compare reasoning quality
2. Identify logical flaws
3. Identify missing considerations
4. Select the best response
5. Explain your decision clearly
"""

DEBATE_FINAL_PROMPT = """\
Respond in the same language as the original question.
{context}
Original question:
{question}

Model responses:
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
        ctx = self.config.get("chat_context", "")
        if ctx:
            return f"\nConversation so far:\n{ctx}\n"
        return ""

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

    # --- Debate mode: N debaters -> Judge evaluates -> Final synthesizes ---

    def _run_debate(self):
        cfg = self.config
        context = self._get_context_block()
        responses = []

        # Stage 1: Debate
        for model in cfg["debate_models"]:
            if self._stopped:
                return
            self.token_update.emit(f"\n=== Debater: {model} ===\n\n")
            answer = self._stream(model, DEBATE_PROMPT.format(
                question=cfg["question"], context=context
            ))
            if self._stopped:
                return
            responses.append(answer)
            self.stage_complete.emit(f"debate:{model}", answer)

        # Stage 2: Judge
        formatted = "\n\n".join(
            f"Response {i + 1}:\n{r}" for i, r in enumerate(responses)
        )
        self.token_update.emit(f"\n\n=== Judge: {cfg['judge_model']} ===\n\n")
        judge_prompt = DEBATE_JUDGE_PROMPT.format(
            question=cfg["question"], responses=formatted, context=context
        )
        judge_output = self._stream(cfg["judge_model"], judge_prompt, temperature=0.3)
        if self._stopped:
            return
        self.stage_complete.emit("judge", judge_output)

        # Stage 3: Final
        self.token_update.emit(f"\n\n=== Final: {cfg['final_model']} ===\n\n")
        final_prompt = DEBATE_FINAL_PROMPT.format(
            question=cfg["question"],
            responses=formatted,
            judge_output=judge_output,
            context=context,
        )
        final_answer = self._stream(cfg["final_model"], final_prompt, temperature=0.5, is_final=True)
        if self._stopped:
            return
        self.stage_complete.emit("final", final_answer)
        self.finished_signal.emit(final_answer)
