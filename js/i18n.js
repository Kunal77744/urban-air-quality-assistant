/**
 * @file i18n.js - Dual-language dictionary (English & Hindi)
 */

export const translations = {
  en: {
    appTitle: "Urban Air Quality Assistant",
    appSubtitle: "Low-Emission Daily Routines & Science-Based Indoor Hacks",
    skipLink: "Skip to main content",
    languageToggle: "हिंदी में देखें",
    cityLabel: "Select or search your city",
    searchPlaceholder: "e.g., Delhi, Mumbai, Bengaluru...",
    commuteLabel: "Daily Commute Mode",
    distanceLabel: "One-Way Distance (km)",
    vulnerableLabel: "Vulnerable household members (infants, elderly, asthma)",
    generatePlanBtn: "Generate Action Plan",
    loadingText: "Calculating air quality & personalized impact...",
    aqiLabel: "Current Air Quality",
    morningSlot: "Morning Routine",
    afternoonSlot: "Afternoon Ventilation",
    eveningSlot: "Evening Protection",
    indoorHacksTitle: "Indoor Air Quality Hacks",
    alternativesTitle: "Sustainable Daily Alternatives",
    impactTitle: "Your Quantified Daily Impact",
    co2SavedLabel: "Estimated CO2 Saved",
    exposureLabel: "PM2.5 Exposure Reduction",
    disclaimer: "Impact estimates calculated using ARAI & WHO scientific baselines. LLMs do not produce numbers.",
    healthDisclaimer: "Disclaimer: This tool provides environmental advice, not direct medical counsel.",
  },
  hi: {
    appTitle: "शहरी वायु गुणवत्ता सहायक",
    appSubtitle: "कम उत्सर्जन वाली दिनचर्या और वैज्ञानिक इनडोर वायु सुधार",
    skipLink: "मुख्य सामग्री पर जाएं",
    languageToggle: "Switch to English",
    cityLabel: "अपना शहर चुनें या खोजें",
    searchPlaceholder: "जैसे: दिल्ली, मुंबई, बेंगलुरु...",
    commuteLabel: "दैनिक यात्रा का साधन",
    distanceLabel: "एकतरफा दूरी (किमी)",
    vulnerableLabel: "घर में संवेदनशील सदस्य (शिशु, बुजुर्ग, अस्थमा)",
    generatePlanBtn: "कार्य योजना तैयार करें",
    loadingText: "वायु गुणवत्ता और प्रभाव की गणना जारी है...",
    aqiLabel: "वर्तमान वायु गुणवत्ता",
    morningSlot: "सुबह की दिनचर्या",
    afternoonSlot: "दोपहर का वेंटिलेशन",
    eveningSlot: "शाम की सुरक्षा",
    indoorHacksTitle: "इनडोर वायु शोधन उपाय",
    alternativesTitle: "सतत और हरित विकल्प",
    impactTitle: "आपका सटीक दैनिक प्रभाव",
    co2SavedLabel: "अनुमानित CO2 बचत",
    exposureLabel: "PM2.5 जोखिम में कमी",
    disclaimer: "प्रभाव की गणना ARAI और WHO के वैज्ञानिक सूत्रों पर आधारित है। LLM संख्याएं नहीं बनाता।",
    healthDisclaimer: "सलाह: यह पर्यावरण सुझाव है, प्रत्यक्ष चिकित्सा परामर्श नहीं।",
  },
};

/**
 * Retrieve translation for key in target language.
 * @param {string} key
 * @param {string} lang
 * @returns {string}
 */
export function t(key, lang = "en") {
  const currentLang = lang === "hi" ? "hi" : "en";
  return translations[currentLang][key] || translations.en[key] || key;
}
