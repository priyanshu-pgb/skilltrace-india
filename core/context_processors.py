def skillbridge_context(request):
    """Global context variables available across all templates."""
    return {
        'BRAND_NAME': 'SkillBridge',
        'BRAND_TAGLINE': 'Assess. Improve. Connect.',
        'BRAND_SUBTITLE': 'Know your real skills. Discover your gaps. Improve your career readiness.',
        'CURRENT_YEAR': 2026,
    }
