"""
数据模型定义模块

定义 kaoyan-english-core 技能使用的所有数据结构和常量。

版本: 2.0.0
创建日期: 2026-03-24
最后更新: 2026-03-24
"""

from datetime import datetime, date
from typing import Dict, List, Any, Optional
from enum import Enum


# 枚举类型定义


class ExamType(Enum):
    """考试类型"""
    ENGLISH_1 = "english_1"
    ENGLISH_2 = "english_2"


class CurrentLevel(Enum):
    """当前英语水平"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ReviewFocus(Enum):
    """复习重点"""
    BALANCED = "balanced"
    POLYSEMY_PRIORITY = "polysemy_priority"
    WRITING_PRIORITY = "writing_priority"


class LearningStyle(Enum):
    """学习风格"""
    CONTEXT_FIRST = "context_first"
    ROTE_FIRST = "rote_first"


class PolysemySensitivity(Enum):
    """僻义敏感度"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MentalStatus(Enum):
    """心理状态"""
    ENERGIZED = "energized"
    NORMAL = "normal"
    TIRED = "tired"
    BURNED_OUT = "burned_out"


class WarningLevel(Enum):
    """预警级别"""
    CRITICAL = "critical"
    WARNING = "warning"
    ATTENTION = "attention"


class ExamFrequency(Enum):
    """考试频率"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# 常量定义

DEFAULT_DAILY_NEW_WORD_TARGET = 50
DEFAULT_POLYSEMY_SENSITIVITY = PolysemySensitivity.MEDIUM
DEFAULT_REVIEW_FOCUS = ReviewFocus.BALANCED
DEFAULT_LEARNING_STYLE = LearningStyle.CONTEXT_FIRST

AUTO_REFRESH_INTERVAL_DAYS = 30

# 僻义检测阈值
POLYSEMY_CRITICAL_THRESHOLD = 0.3
POLYSEMY_WARNING_THRESHOLD = 0.5

# SM-2 算法默认参数
SM2_DEFAULT_EASE_FACTOR = 2.5
SM2_MIN_EASE_FACTOR = 1.3
SM2_DEFAULT_INTERVAL = 1


# 数据模型类


class UserProfile:
    """用户画像数据模型"""

    def __init__(
        self,
        user_id: str,
        conversation_id: str,
        exam_date: date,
        exam_type: ExamType = ExamType.ENGLISH_2,
        target_score: int = 75,
        current_level: CurrentLevel = CurrentLevel.INTERMEDIATE,
        daily_new_word_target: int = DEFAULT_DAILY_NEW_WORD_TARGET,
        review_focus: ReviewFocus = DEFAULT_REVIEW_FOCUS,
        learning_style: LearningStyle = DEFAULT_LEARNING_STYLE,
        polysemy_sensitivity: PolysemySensitivity = DEFAULT_POLYSEMY_SENSITIVITY
    ):
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # 考试信息
        self.exam_date = exam_date
        self.exam_type = exam_type
        self.target_score = target_score
        self.current_level = current_level

        # 词汇基础
        self.total_words = 0
        self.mastered_count = 0
        self.reviewing_count = 0
        self.new_count = 0

        # 偏好设置
        self.daily_new_word_target = daily_new_word_target
        self.review_focus = review_focus
        self.learning_style = learning_style
        self.polysemy_sensitivity = polysemy_sensitivity

        # 心理历史
        self.mental_history: List[Dict[str, Any]] = []

        # 刷新配置
        self.last_refreshed = date.today()
        self.auto_refresh_interval = AUTO_REFRESH_INTERVAL_DAYS
        self.pending_refresh = False

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "user_id": self.user_id,
            "conversation_id": self.conversation_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),

            # 考试信息
            "exam_date": self.exam_date.isoformat(),
            "exam_type": self.exam_type.value,
            "target_score": self.target_score,
            "current_level": self.current_level.value,

            # 词汇基础
            "vocabulary_base": {
                "total_words": self.total_words,
                "mastered_count": self.mastered_count,
                "reviewing_count": self.reviewing_count,
                "new_count": self.new_count
            },

            # 偏好设置
            "preferences": {
                "daily_new_word_target": self.daily_new_word_target,
                "review_focus": self.review_focus.value,
                "learning_style": self.learning_style.value,
                "polysemy_sensitivity": self.polysemy_sensitivity.value
            },

            # 心理历史
            "mental_history": self.mental_history,

            # 刷新配置
            "refresh_config": {
                "last_refreshed": self.last_refreshed.isoformat(),
                "auto_refresh_interval": self.auto_refresh_interval,
                "pending_refresh": self.pending_refresh
            }
        }


class WordCard:
    """词汇卡片数据模型（SM-2 + 考研适配）"""

    def __init__(
        self,
        word: str,
        user_id: str,
        ease_factor: float = SM2_DEFAULT_EASE_FACTOR,
        interval: int = SM2_DEFAULT_INTERVAL,
        exam_date: Optional[date] = None
    ):
        # 基础信息
        self.word = word
        self.user_id = user_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # SM-2基础字段
        self.ease_factor = ease_factor
        self.interval = interval
        self.review_count = 0
        self.next_review: Optional[date] = None
        self.correct_count = 0
        self.incorrect_count = 0
        self.forgetting_rate = 0.0

        # 考研适配字段
        self.exam_date = exam_date
        self.current_phase = ""
        self.phase_factor = 1.0
        self.days_to_exam = 0
        self.adjusted_interval = interval

        # 僻义预警字段
        self.polysemy_alert = False
        self.warning_level: Optional[WarningLevel] = None
        self.exam_frequency: Optional[ExamFrequency] = None
        self.rare_meanings: List[str] = []
        self.common_meanings: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            # 基础信息
            "word": self.word,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),

            # SM-2基础字段
            "ease_factor": self.ease_factor,
            "interval": self.interval,
            "review_count": self.review_count,
            "next_review": self.next_review.isoformat() if self.next_review else None,
            "correct_count": self.correct_count,
            "incorrect_count": self.incorrect_count,
            "forgetting_rate": self.forgetting_rate,

            # 考研适配字段
            "exam_date": self.exam_date.isoformat() if self.exam_date else None,
            "current_phase": self.current_phase,
            "phase_factor": self.phase_factor,
            "days_to_exam": self.days_to_exam,
            "adjusted_interval": self.adjusted_interval,

            # 僻义预警字段
            "polysemy_alert": self.polysemy_alert,
            "warning_level": self.warning_level.value if self.warning_level else None,
            "exam_frequency": self.exam_frequency.value if self.exam_frequency else None,
            "rare_meanings": self.rare_meanings,
            "common_meanings": self.common_meanings
        }


class ReviewRecord:
    """复习记录数据模型"""

    def __init__(
        self,
        user_id: str,
        record_id: Optional[str] = None,
        review_date: Optional[date] = None
    ):
        self.record_id = record_id or f"review_{user_id}_{datetime.now().timestamp()}"
        self.user_id = user_id
        self.date = review_date or date.today()
        self.created_at = datetime.now()

        # 会话信息
        self.words_reviewed = 0
        self.new_words = 0
        self.duration_minutes = 0

        # 结果统计
        self.correct_count = 0
        self.incorrect_count = 0
        self.polysemy_errors = 0

        # 阶段上下文
        self.current_phase = ""
        self.days_to_exam = 0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "record_id": self.record_id,
            "user_id": self.user_id,
            "date": self.date.isoformat(),
            "created_at": self.created_at.isoformat(),

            # 会话信息
            "session_info": {
                "words_reviewed": self.words_reviewed,
                "new_words": self.new_words,
                "duration_minutes": self.duration_minutes
            },

            # 结果统计
            "results": {
                "correct_count": self.correct_count,
                "incorrect_count": self.incorrect_count,
                "polysemy_errors": self.polysemy_errors
            },

            # 阶段上下文
            "phase_context": {
                "current_phase": self.current_phase,
                "days_to_exam": self.days_to_exam
            }
        }


class MentalStateRecord:
    """心理状态记录数据模型"""

    def __init__(
        self,
        date: date,
        status: MentalStatus,
        vocabulary_fatigue: float = 0.5,
        trigger: str = ""
    ):
        self.date = date
        self.status = status
        self.vocabulary_fatigue = max(0.0, min(1.0, vocabulary_fatigue))
        self.trigger = trigger

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "date": self.date.isoformat(),
            "status": self.status.value,
            "vocabulary_fatigue": self.vocabulary_fatigue,
            "trigger": self.trigger
        }


# 导出的公共类和常量
__all__ = [
    # 枚举类型
    "ExamType",
    "CurrentLevel",
    "ReviewFocus",
    "LearningStyle",
    "PolysemySensitivity",
    "MentalStatus",
    "WarningLevel",
    "ExamFrequency",

    # 常量
    "DEFAULT_DAILY_NEW_WORD_TARGET",
    "DEFAULT_POLYSEMY_SENSITIVITY",
    "DEFAULT_REVIEW_FOCUS",
    "DEFAULT_LEARNING_STYLE",
    "AUTO_REFRESH_INTERVAL_DAYS",
    "POLYSEMY_CRITICAL_THRESHOLD",
    "POLYSEMY_WARNING_THRESHOLD",
    "SM2_DEFAULT_EASE_FACTOR",
    "SM2_MIN_EASE_FACTOR",
    "SM2_DEFAULT_INTERVAL",

    # 数据模型类
    "UserProfile",
    "WordCard",
    "ReviewRecord",
    "MentalStateRecord",
]
