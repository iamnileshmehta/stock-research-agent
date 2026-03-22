from .models import AgentState, CriticResult


class Critic:
    def review(self, state: AgentState) -> CriticResult:
        notes: list[str] = []

        if not state.observations:
            return CriticResult(passed=False, score=0, notes=["No tool outputs were generated."])

        failed = [o for o in state.observations if o.status != "success"]
        if failed:
            notes.append(f"{len(failed)} step(s) failed. Verify data/provider availability.")

        has_technical = any(o.tool == "run_technical_analysis" and o.status == "success" for o in state.observations)
        has_fundamental = any(o.tool == "run_fundamental_analysis" and o.status == "success" for o in state.observations)

        if not has_technical:
            notes.append("Technical analysis missing.")
        if not has_fundamental:
            notes.append("Fundamental analysis missing or partial.")

        score = 100
        score -= 25 * len(failed)
        if not has_technical:
            score -= 30
        if not has_fundamental:
            score -= 20
        score = max(0, min(100, score))

        if score < 70:
            notes.append("Confidence reduced due to incomplete evidence.")

        return CriticResult(passed=score >= 70, score=score, notes=notes)
