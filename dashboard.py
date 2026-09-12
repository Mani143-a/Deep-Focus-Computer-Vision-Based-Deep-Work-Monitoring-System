from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from app.analytics.session_history import SessionHistory


# =============================================================
# CONFIGURATION
# =============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"

st.set_page_config(
    page_title="DeepFocus Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================
# STYLING
# =============================================================

st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
        }

        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 10px;
            padding: 15px;
        }

        .dashboard-subtitle {
            color: #777;
            margin-top: -15px;
            margin-bottom: 25px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================
# HELPERS
# =============================================================


def format_duration(seconds: float) -> str:
    """Convert seconds into a human-readable duration."""

    seconds = max(0.0, float(seconds))

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"

    if minutes > 0:
        return f"{minutes}m {secs}s"

    return f"{secs}s"


def format_percentage(value: float) -> str:
    """Format a percentage."""

    return f"{float(value):.1f}%"


def load_history() -> SessionHistory:
    """Load session history safely."""

    history = SessionHistory(
        reports_dir=REPORTS_DIR,
    )

    history.load_valid()

    return history


def discover_csv_files() -> list[Path]:
    """Return available session CSV files."""

    if not DATA_DIR.exists():
        return []

    return sorted(
        DATA_DIR.glob("session_*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def load_session_csv(path: Path) -> pd.DataFrame:
    """Load one session CSV safely."""

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        st.error(
            f"Could not read session CSV: {path.name}\n\n{exc}"
        )
        return pd.DataFrame()

    return df


def find_column(
    df: pd.DataFrame,
    candidates: list[str],
) -> str | None:
    """Find the first matching column."""

    for candidate in candidates:
        if candidate in df.columns:
            return candidate

    return None


# =============================================================
# HEADER
# =============================================================

st.title("🎯 DeepFocus")

st.markdown(
    '<p class="dashboard-subtitle">'
    "Personal Deep-Work Monitoring & Session Analytics"
    "</p>",
    unsafe_allow_html=True,
)


# =============================================================
# LOAD DATA
# =============================================================

history = load_history()
reports = list(history.reports)

csv_files = discover_csv_files()


# =============================================================
# SIDEBAR
# =============================================================

st.sidebar.title("DeepFocus")

st.sidebar.caption(
    "Computer-vision based deep-work monitoring"
)

st.sidebar.divider()

if st.sidebar.button(
    "🔄 Refresh Dashboard",
    use_container_width=True,
):
    st.rerun()

st.sidebar.divider()

st.sidebar.subheader("Data")

st.sidebar.write(
    f"Reports: **{len(reports)}**"
)

st.sidebar.write(
    f"CSV sessions: **{len(csv_files)}**"
)

st.sidebar.divider()

st.sidebar.subheader("Navigation")

page = st.sidebar.radio(
    "View",
    [
        "Overview",
        "Session Detail",
        "History",
    ],
)


# =============================================================
# EMPTY STATE
# =============================================================

if not reports:

    st.warning(
        "No session reports are available yet."
    )

    st.info(
        "Run a DeepFocus monitoring session first. "
        "The finalized SessionReport will be saved "
        "inside data/reports/."
    )

    st.stop()


# =============================================================
# OVERVIEW
# =============================================================

if page == "Overview":

    summary = history.summary()

    st.header("Session Overview")

    st.caption(
        "Aggregate analytics across all recorded sessions."
    )

    # ---------------------------------------------------------
    # TOP METRICS
    # ---------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Sessions",
            summary.total_sessions,
        )

    with col2:
        st.metric(
            "Total Study Time",
            format_duration(
                summary.total_session_time
            ),
        )

    with col3:
        st.metric(
            "Total Focus Time",
            format_duration(
                summary.total_focus_time
            ),
        )

    with col4:
        st.metric(
            "Average Focus",
            format_percentage(
                summary.average_focus_percentage
            ),
        )

    st.divider()

    # ---------------------------------------------------------
    # SECONDARY METRICS
    # ---------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Average Session",
            format_duration(
                summary.average_session_duration
            ),
        )

    with col2:
        st.metric(
            "Total Unfocused",
            format_duration(
                summary.total_unfocused_time
            ),
        )

    with col3:
        if summary.best_session is not None:
            st.metric(
                "Best Focus",
                format_percentage(
                    summary.best_session.focus_percentage
                ),
            )
        else:
            st.metric(
                "Best Focus",
                "N/A",
            )

    with col4:
        if summary.worst_session is not None:
            st.metric(
                "Lowest Focus",
                format_percentage(
                    summary.worst_session.focus_percentage
                ),
            )
        else:
            st.metric(
                "Lowest Focus",
                "N/A",
            )

    st.divider()

    # ---------------------------------------------------------
    # RECENT SESSION TABLE
    # ---------------------------------------------------------

    st.subheader("Recent Sessions")

    recent_reports = history.recent(
        min(10, len(reports))
    )

    recent_rows = []

    for index, report in enumerate(
        recent_reports,
        start=1,
    ):
        recent_rows.append(
            {
                "Session": index,
                "Duration": format_duration(
                    report.session_duration
                ),
                "Focus": format_percentage(
                    report.focus_percentage
                ),
                "Score": f"{report.session_score:.1f}",
                "Eye Closures": report.eye_closure_count,
                "Face Losses": report.face_loss_count,
            }
        )

    if recent_rows:
        st.dataframe(
            pd.DataFrame(recent_rows),
            use_container_width=True,
            hide_index=True,
        )

    # ---------------------------------------------------------
    # BEST / WORST
    # ---------------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏆 Best Session")

        best = summary.best_session

        if best is not None:

            st.metric(
                "Focus",
                format_percentage(
                    best.focus_percentage
                ),
            )

            st.write(
                f"Duration: "
                f"**{format_duration(best.session_duration)}**"
            )

            st.write(
                f"Score: "
                f"**{best.session_score:.1f}/100**"
            )

    with col2:

        st.subheader("⚠️ Lowest Focus Session")

        worst = summary.worst_session

        if worst is not None:

            st.metric(
                "Focus",
                format_percentage(
                    worst.focus_percentage
                ),
            )

            st.write(
                f"Duration: "
                f"**{format_duration(worst.session_duration)}**"
            )

            st.write(
                f"Score: "
                f"**{worst.session_score:.1f}/100**"
            )


# =============================================================
# SESSION DETAIL
# =============================================================

elif page == "Session Detail":

    st.header("Session Detail")

    st.caption(
        "Inspect the detailed signal data from a recorded session."
    )

    if not csv_files:

        st.warning(
            "No session CSV files were found."
        )

        st.stop()

    selected_csv = st.selectbox(
        "Select session",
        csv_files,
        format_func=lambda path: path.stem,
    )

    df = load_session_csv(
        selected_csv
    )

    if df.empty:
        st.stop()

    st.write(
        f"**File:** `{selected_csv.name}`"
    )

    st.write(
        f"**Rows:** `{len(df):,}`"
    )

    # ---------------------------------------------------------
    # RAW DATA
    # ---------------------------------------------------------

    st.subheader("Session Data")

    st.dataframe(
        df.tail(1000),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ---------------------------------------------------------
    # SIGNAL COLUMNS
    # ---------------------------------------------------------

    elapsed_column = find_column(
        df,
        [
            "elapsed_seconds",
            "elapsed",
            "timestamp",
            "time",
        ],
    )

    raw_ear_column = find_column(
        df,
        [
            "raw_ear",
            "ear",
        ],
    )

    smooth_ear_column = find_column(
        df,
        [
            "smoothed_ear",
            "smooth_ear",
        ],
    )

    state_column = find_column(
        df,
        [
            "state",
            "focus_state",
            "focusstate",
        ],
    )

    # ---------------------------------------------------------
    # EAR CHART
    # ---------------------------------------------------------

    if (
        elapsed_column is not None
        and (
            raw_ear_column is not None
            or smooth_ear_column is not None
        )
    ):

        st.subheader("Eye Aspect Ratio")

        chart_columns = []

        if raw_ear_column is not None:
            chart_columns.append(
                raw_ear_column
            )

        if smooth_ear_column is not None:
            chart_columns.append(
                smooth_ear_column
            )

        ear_df = df[
            [elapsed_column] + chart_columns
        ].copy()

        ear_df = ear_df.rename(
            columns={
                elapsed_column: "Time"
            }
        )

        ear_df = ear_df.set_index(
            "Time"
        )

        st.line_chart(
            ear_df,
            use_container_width=True,
        )

    # ---------------------------------------------------------
    # STATE DISTRIBUTION
    # ---------------------------------------------------------

    if state_column is not None:

        st.subheader("State Distribution")

        state_counts = (
            df[state_column]
            .astype(str)
            .value_counts()
        )

        state_data = (
            state_counts
            .rename("Frames")
            .to_frame()
        )

        st.bar_chart(
            state_data,
            use_container_width=True,
        )

    # ---------------------------------------------------------
    # SESSION SUMMARY
    # ---------------------------------------------------------

    st.divider()

    st.subheader("Session Summary")

    selected_report = None

    if reports:

        # Match report approximately using session order.
        selected_report = reports[-1]

    if selected_report is not None:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Focus",
                format_percentage(
                    selected_report.focus_percentage
                ),
            )

        with col2:
            st.metric(
                "Score",
                f"{selected_report.session_score:.1f}/100",
            )

        with col3:
            st.metric(
                "Eye Closures",
                selected_report.eye_closure_count,
            )

        with col4:
            st.metric(
                "Face Losses",
                selected_report.face_loss_count,
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(
                "**Focused:** "
                f"{format_duration(selected_report.focused_duration)}"
            )

        with col2:
            st.write(
                "**Unfocused:** "
                f"{format_duration(selected_report.unfocused_duration)}"
            )

        with col3:
            st.write(
                "**Eyes Closed:** "
                f"{format_duration(selected_report.total_closed_time)}"
            )

        st.write(
            "**Longest Eye Closure:** "
            f"{selected_report.longest_closure:.2f}s"
        )

        st.write(
            "**Average Eye Closure:** "
            f"{selected_report.average_closure:.2f}s"
        )


# =============================================================
# HISTORY
# =============================================================

elif page == "History":

    st.header("Session History")

    st.caption(
        "Historical performance across recorded DeepFocus sessions."
    )

    if len(reports) == 0:

        st.info(
            "No historical sessions available."
        )

        st.stop()

    # ---------------------------------------------------------
    # BUILD HISTORY DATAFRAME
    # ---------------------------------------------------------

    rows = []

    for index, report in enumerate(
        reports,
        start=1,
    ):

        rows.append(
            {
                "Session": index,
                "Duration (min)": (
                    report.session_duration / 60.0
                ),
                "Focus (%)": report.focus_percentage,
                "Score": report.session_score,
                "Focused (min)": (
                    report.focused_duration / 60.0
                ),
                "Unfocused (min)": (
                    report.unfocused_duration / 60.0
                ),
                "Eye Closures": (
                    report.eye_closure_count
                ),
                "Closed Time (s)": (
                    report.total_closed_time
                ),
                "Face Losses": (
                    report.face_loss_count
                ),
            }
        )

    history_df = pd.DataFrame(rows)

    # ---------------------------------------------------------
    # FOCUS TREND
    # ---------------------------------------------------------

    st.subheader("Focus Trend")

    focus_chart = history_df[
        ["Session", "Focus (%)"]
    ].set_index("Session")

    st.line_chart(
        focus_chart,
        use_container_width=True,
    )

    # ---------------------------------------------------------
    # SESSION SCORE
    # ---------------------------------------------------------

    st.subheader("Session Score")

    score_chart = history_df[
        ["Session", "Score"]
    ].set_index("Session")

    st.bar_chart(
        score_chart,
        use_container_width=True,
    )

    # ---------------------------------------------------------
    # DURATION VS FOCUS
    # ---------------------------------------------------------

    st.subheader("Session Duration vs Focus")

    duration_focus = history_df[
        [
            "Session",
            "Duration (min)",
            "Focus (%)",
        ]
    ].set_index("Session")

    st.dataframe(
        duration_focus,
        use_container_width=True,
    )

    # ---------------------------------------------------------
    # FULL HISTORY
    # ---------------------------------------------------------

    st.subheader("All Sessions")

    display_df = history_df.copy()

    numeric_columns = [
        "Duration (min)",
        "Focus (%)",
        "Score",
        "Focused (min)",
        "Unfocused (min)",
        "Closed Time (s)",
    ]

    for column in numeric_columns:
        display_df[column] = display_df[
            column
        ].round(2)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


# =============================================================
# FOOTER
# =============================================================

st.divider()

st.caption(
    "DeepFocus | Computer Vision Deep-Work Monitoring System"
)