from datetime import date

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.company import Company
from app.models.feedback import CategoryBreakdown, MoodHeatmapCell, SentimentDailyStat
from app.models.issue import Issue
from app.models.notification_setting import NotificationSetting
from app.models.recommendation import Recommendation
from app.models.report import ComparisonMetric, Report
from app.models.user import User

DEMO_EMAIL = "jamie@acmecorp.com"
DEMO_PASSWORD = "InsightFlow123"

TREND = [
    (date(2026, 6, 21), 64, 22, 14),
    (date(2026, 6, 22), 67, 20, 13),
    (date(2026, 6, 23), 65, 23, 12),
    (date(2026, 6, 24), 70, 18, 12),
    (date(2026, 6, 25), 68, 21, 11),
    (date(2026, 6, 26), 72, 17, 11),
    (date(2026, 6, 27), 71, 18, 11),
]

CATEGORIES = [
    ("Product", 38, "#7c6dff"),
    ("Support", 24, "#ff7c47"),
    ("UX", 22, "#00d4aa"),
    ("Pricing", 16, "#ff5fa0"),
]

HEATMAP = [3, 5, 4, 7, 6, 2, 1, 4, 6, 5, 8, 7, 3, 2, 5, 7, 9, 8, 6, 4, 3, 4, 5, 6, 7, 5, 3, 2, 3, 4, 5, 6, 5, 3, 2]

ISSUES = [
    ("Checkout friction", 34, "#ff7c47"),
    ("Page load speed", 28, "#7c6dff"),
    ("Mobile layout", 22, "#ff5fa0"),
    ("Missing features", 19, "#a99dff"),
    ("Pricing clarity", 14, "#00d4aa"),
    ("Support response", 11, "#ffb347"),
]

RECOMMENDATIONS = [
    ("high", "Simplify checkout flow.", "34 users cited payment friction. A/B test one-click checkout — estimated recovery of $12K/mo in abandoned carts."),
    ("med", "Improve onboarding emails.", "18 users felt confused in first 48 hours. Add a 3-step welcome sequence with quick-start prompts."),
    ("med", "Add dark mode.", "Mentioned 22 times across product reviews. High satisfaction lift potential for power users and developers."),
    ("low", "Expand CSV export options.", "11 users requested more flexible export formats. Would reduce support tickets by an estimated 8%."),
]

REPORTS = [
    ("Weekly Sentiment Summary", "AI-curated digest of all feedback this week with top themes, mood scores, and priority alerts.", "📊", "rgba(124,109,255,0.12)", date(2026, 6, 10)),
    ("Issues & Urgency Report", "All flagged issues ranked by frequency, sentiment impact, and estimated revenue effect on your business.", "🔥", "rgba(255,124,71,0.12)", date(2026, 6, 9)),
    ("30-Day Trend Analysis", "Long-form trend report covering satisfaction movement, NPS shifts, and category distribution changes.", "📈", "rgba(0,212,170,0.12)", date(2026, 6, 1)),
    ("AI Improvement Suggestions", "Full list of AI-generated product and CX recommendations with supporting data evidence and priority scores.", "💡", "rgba(255,95,160,0.12)", date(2026, 6, 7)),
    ("Team Performance Report", "Support team response rates, average resolution times, and customer satisfaction scores per agent.", "👥", "rgba(124,109,255,0.12)", date(2026, 6, 3)),
    ("Source Comparison Report", "Feedback quality, volume, and sentiment differences across all connected data sources and channels.", "🌐", "rgba(255,124,71,0.12)", date(2026, 6, 1)),
]

COMPARISON = [
    ("Avg Sentiment", "May 2026", 8.3, "8.3", "June 2026", 8.7, "8.7 ↑", "up"),
    ("Positive Rate", "May 2026", 65, "65%", "June 2026", 72, "72% ↑", "up"),
    ("Issues Flagged", "May 2026", 59, "59", "June 2026", 47, "47 ↓", "down"),
    ("Feedback Volume", "May 2026", 10800, "10.8K", "June 2026", 12800, "12.8K ↑", "up"),
    ("Resolution Time", "May 2026", 4.2, "4.2 hrs", "June 2026", 3.1, "3.1 hrs ↓", "down"),
]

NOTIFICATIONS = [
    ("weekly_digest", "Weekly AI insight email", "Every Monday morning with your weekly digest", True),
    ("high_priority_alerts", "High-priority issue alerts", "Instant alerts when a critical pattern emerges", True),
    ("sentiment_drop_warnings", "Sentiment drop warnings", "Alert if your score drops more than 0.5 pts in a day", False),
]

TEAM = [
    ("Jamie Scott", DEMO_EMAIL, "admin"),
    ("Maya Kim", "maya@acmecorp.com", "editor"),
    ("Tom Reeves", "tom@acmecorp.com", "viewer"),
]


def seed_initial_data() -> None:
    db = SessionLocal()
    try:
        if db.query(Company).first():
            return

        company = Company(
            name="Acme Corp",
            industry="E-Commerce / Retail",
            primary_email="team@acmecorp.com",
            timezone="UTC+0 — London",
            website="https://acmecorp.com",
            language="English (UK)",
            plan_name="Pro",
            plan_price=89.0,
            responses_used=7234,
            responses_limit=10000,
            seats_used=3,
            seats_limit=5,
        )
        db.add(company)
        db.flush()

        for name, email, role in TEAM:
            db.add(User(
                name=name,
                email=email,
                role=role,
                hashed_password=hash_password(DEMO_PASSWORD),
                company_id=company.id,
            ))

        for stat_date, pos, neu, neg in TREND:
            db.add(SentimentDailyStat(stat_date=stat_date, positive_pct=pos, neutral_pct=neu, negative_pct=neg))

        for category, pct, color in CATEGORIES:
            db.add(CategoryBreakdown(category=category, percentage=pct, color=color))

        for idx, score in enumerate(HEATMAP):
            db.add(MoodHeatmapCell(week_index=idx // 7, day_index=idx % 7, score=score))

        for rank, (label, count, color) in enumerate(ISSUES, start=1):
            db.add(Issue(label=label, count=count, color=color, rank=rank))

        for priority, title, detail in RECOMMENDATIONS:
            db.add(Recommendation(priority=priority, title=title, detail=detail))

        for title, description, icon, icon_bg, report_date in REPORTS:
            db.add(Report(title=title, description=description, icon=icon, icon_bg=icon_bg, report_date=report_date))

        for metric_name, prev_label, prev_val, prev_disp, cur_label, cur_val, cur_disp, trend in COMPARISON:
            db.add(ComparisonMetric(
                metric_name=metric_name,
                previous_label=prev_label,
                previous_value=prev_val,
                previous_display=prev_disp,
                current_label=cur_label,
                current_value=cur_val,
                current_display=cur_disp,
                trend=trend,
            ))

        for key, label, description, enabled in NOTIFICATIONS:
            db.add(NotificationSetting(company_id=company.id, key=key, label=label, description=description, enabled=enabled))

        db.commit()
    finally:
        db.close()
