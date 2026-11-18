"""Helper routines and catalog data for routine planner."""

from models.air_quality import AirQualityData
from models.routine_plan import IndoorHack, RoutineItem
from models.user_profile import ExerciseHabit, UserProfile


def _build_morning(
    poor: bool, risk: bool, indoor_only: bool, is_hi: bool
) -> RoutineItem:
    """Create morning routine item."""
    if poor or risk or indoor_only:
        act = "घर के अंदर प्राणायाम/हल्का व्यायाम करें" if is_hi else "Shift workout indoors"
        why = (
            "सुबह जमीनी हवा में PM2.5 सबसे सघन होता है"
            if is_hi
            else "Morning inversion traps heavy PM2.5 near ground"
        )
    else:
        act = (
            "सुबह 7-8 बजे के बाद ही बाहर निकलें"
            if is_hi
            else "Outdoor run safe before traffic peak"
        )
        why = "AQI मध्यम स्तर पर है" if is_hi else "AQI is currently moderate"
    return RoutineItem(
        slot="morning", action=act, why=why, exposure_impact="-35% PM2.5 peak exposure"
    )


def _build_afternoon(is_hi: bool) -> RoutineItem:
    """Create afternoon routine item."""
    act = (
        "दोपहर 12 से 3 के बीच वेंटिलेशन करें" if is_hi else "Open windows between 12 PM - 3 PM"
    )
    why = (
        "धूप और हवा से दोपहर में प्रदूषण कम होता है"
        if is_hi
        else "Thermal convection disperses surface particulates"
    )
    return RoutineItem(
        slot="afternoon", action=act, why=why, exposure_impact="-25% indoor stagnation"
    )


def _build_evening(is_hi: bool) -> RoutineItem:
    """Create evening routine item."""
    act = (
        "शाम 6-9 बजे खिड़कियां बंद रखें व मास्क पहनें"
        if is_hi
        else "Seal windows & wear N95 during evening rush"
    )
    why = (
        "शाम के ट्रैफिक और ठंडी हवा से धुंध बढ़ती है"
        if is_hi
        else "Evening rush hour causes secondary pollution peak"
    )
    return RoutineItem(
        slot="evening", action=act, why=why, exposure_impact="-40% rush-hour inhalation"
    )


def generate_time_routines(
    aqi_data: AirQualityData,
    profile: UserProfile,
    is_hi: bool,
) -> list[RoutineItem]:
    """Create morning, afternoon, and evening routines based on AQI."""
    is_poor = aqi_data.aqi > 150
    high_risk = profile.has_vulnerable_members or profile.has_asthma_or_respiratory
    indoor_only = profile.exercise_habit == ExerciseHabit.INDOOR

    return [
        _build_morning(is_poor, high_risk, indoor_only, is_hi),
        _build_afternoon(is_hi),
        _build_evening(is_hi),
    ]


def _get_hacks_en() -> list[IndoorHack]:
    """Return English indoor hacks catalog."""
    return [
        IndoorHack(
            category="ventilation",
            title="Afternoon Cross-Ventilation",
            description="Flush indoor CO2 by opening windows 20 mins between 12-3 PM when surface PM2.5 is lowest.",
        ),
        IndoorHack(
            category="filtration",
            title="DIY Corsi-Rosenthal Box",
            description="A box fan with 4 MERV-13 filters delivers CADR comparable to commercial HEPA at 1/5th cost.",
        ),
        IndoorHack(
            category="cooking",
            title="Cookware Lids & Range Hood",
            description="Frying creates ultrafine particles; lids and post-cook exhaust run reduce peaks by 65%.",
        ),
        IndoorHack(
            category="cleaning",
            title="Wet Mopping vs Dry Sweeping",
            description="Dry sweeping aerosolizes settled PM10; microfiber wet mopping captures 85% of floor dust.",
            fact_check="Myth Buster: Houseplants remove negligible PM2.5 in real homes; mechanical filters are required.",
        ),
    ]


def _get_hacks_hi() -> list[IndoorHack]:
    """Return Hindi indoor hacks catalog."""
    return [
        IndoorHack(
            category="ventilation",
            title="दुपहर वेंटिलेशन नियम",
            description="दोपहर 12 से 3 बजे के बीच 20 मिनट के लिए खिड़कियां खोलें।",
        ),
        IndoorHack(
            category="filtration",
            title="DIY कोर्सी-रोसेन्थाल बॉक्स",
            description="बॉक्स फैन और MERV-13 फिल्टर से ₹2500 में 90% PM2.5 फिल्टर करें।",
        ),
        IndoorHack(
            category="cooking",
            title="रसोई वेंटिलेशन और कवर",
            description="खाना बनाते समय ढक्कन लगाएं और एग्जॉस्ट फैन 10 मिनट बाद तक चलाएं।",
        ),
        IndoorHack(
            category="cleaning",
            title="गीला पोछा vs सूखी झाड़ू",
            description="सूखी झाड़ू से धूल के कण हवा में उड़ते हैं; गीले पोछे का प्रयोग करें।",
            fact_check="पौधों का भ्रम: पौधे VOCs पर मामूली असर करते हैं, पर PM2.5 कम नहीं कर सकते।",
        ),
    ]


def generate_indoor_hacks(is_hi: bool) -> list[IndoorHack]:
    """Return actionable evidence-based indoor air quality hacks."""
    return _get_hacks_hi() if is_hi else _get_hacks_en()
