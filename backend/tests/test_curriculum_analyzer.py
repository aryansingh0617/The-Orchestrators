from app.infrastructure.ai import StubProvider
from app.modules.curriculum_analyzer import CurriculumAnalyzer


class FailingProvider:
    provider_name = "failing"

    def generate_structured(self, *args, **kwargs):
        raise RuntimeError("provider down")


def test_curriculum_analyzer_reads_supplied_structure() -> None:
    analyzer = CurriculumAnalyzer(StubProvider())
    curriculum = {
        "modules": [
            {
                "name": "RAG Foundations",
                "days": [
                    {
                        "day": 1,
                        "topic": "RAG",
                        "learning_objective": "Build a grounded RAG pipeline",
                        "tools": ["embeddings"],
                        "prerequisites": [],
                    },
                    {
                        "day": 2,
                        "topic": "Chunking",
                        "learning_objective": "Tune chunk size",
                        "tools": ["chunkers"],
                        "prerequisites": [1],
                    },
                ],
            }
        ]
    }

    result = analyzer.analyze(
        role_title="AI Engineer",
        seniority="senior",
        curriculum_data=curriculum,
    )

    assert len(result.curriculum_days) == 2
    assert result.curriculum_days[0].day == 1
    assert result.curriculum_days[0].topic == "RAG"
    assert result.curriculum_days[0].learning_objective
    assert result.curriculum_days[0].tools == ["embeddings"]
    assert "RAG Foundations" in result.priority_levels
    assert result.mission_family_recommendations
    assert result.out_of_scope_topics


def test_curriculum_analyzer_loads_default_fixture() -> None:
    analyzer = CurriculumAnalyzer(StubProvider())
    result = analyzer.analyze(role_title="AI Engineer", seniority="mid")
    assert len(result.curriculum_days) >= 4
    assert result.competencies
    assert result.expected_seniority_bar == "mid"


def test_curriculum_analyzer_provider_failure_falls_back() -> None:
    analyzer = CurriculumAnalyzer(FailingProvider())  # type: ignore[arg-type]
    result = analyzer.analyze(
        role_title="AI Engineer",
        seniority="junior",
        curriculum_data={
            "modules": [
                {
                    "name": "Vector Databases",
                    "days": [
                        {
                            "day": 3,
                            "topic": "HNSW",
                            "learning_objective": "Choose indexes",
                            "tools": ["hnsw"],
                            "prerequisites": [],
                        }
                    ],
                }
            ]
        },
    )
    assert result.curriculum_days[0].day == 3
    assert result.competencies
