from app.application.dtos import InterviewCommand, InterviewResult
from app.core.clock import Clock
from app.core.ids import IdGenerator
from app.domain.entities.assessment import AssessmentSession, SessionStatus
from app.domain.errors import NotFoundError, ValidationError
from app.domain.interfaces import AIProvider, SessionRepository, StructuredGenerationOptions


class InterviewService:
    """Application service for the public interview endpoint contract.

    Milestone 3 intentionally stops at contract-level orchestration. Full planning,
    mission generation, world-state updates, and evaluation are later milestones.
    """

    def __init__(
        self,
        sessions: SessionRepository,
        ai_provider: AIProvider,
        clock: Clock,
        id_generator: IdGenerator,
    ) -> None:
        self._sessions = sessions
        self._ai_provider = ai_provider
        self._clock = clock
        self._id_generator = id_generator

    def handle(self, command: InterviewCommand) -> InterviewResult:
        existing = self._sessions.get_by_external_id(command.session_id)
        if command.candidate is not None and existing is None:
            return self._start_interview(command)
        if existing is None:
            raise NotFoundError(
                "Start the interview with candidate data before sending messages.",
                details={"sessionId": command.session_id},
            )
        if not command.message or not command.message.strip():
            raise ValidationError(
                "A non-empty message is required for an active interview turn.",
                details={"sessionId": command.session_id},
            )
        return self._continue_interview(command)

    def _start_interview(self, command: InterviewCommand) -> InterviewResult:
        if command.candidate is None:
            raise ValidationError("Candidate data is required to start an interview.")

        now = self._clock.now()
        member = command.candidate.member
        session = AssessmentSession(
            id=self._id_generator.new_id(),
            external_session_id=command.session_id,
            candidate_id=member.id,
            role_title=member.jobRole or "AI Engineer",
            seniority=self._infer_seniority(member.yearsExperience),
            status=SessionStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        self._sessions.save(session)
        return InterviewResult(
            reply="Welcome. Let's begin your interview.",
            done=False,
        )

    def _continue_interview(self, command: InterviewCommand) -> InterviewResult:
        result = self._ai_provider.generate_structured(
            prompt=command.message or "",
            schema=InterviewResult,
            options=StructuredGenerationOptions(metadata={"sessionId": command.session_id}),
        )
        return InterviewResult.model_validate(result.data)

    @staticmethod
    def _infer_seniority(years_experience: int | None) -> str:
        if years_experience is None:
            return "mid"
        if years_experience >= 12:
            return "staff"
        if years_experience >= 6:
            return "senior"
        if years_experience >= 2:
            return "mid"
        return "junior"
