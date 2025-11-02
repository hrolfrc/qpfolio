def render_report(frontier_df, images: dict[str, str] | None, out_html: str):
    """
    images: dict keys like {"frontier_png": ".../frontier.png", "weights_png": ".../weights.png"}
    Writes a self-contained HTML with summary tables and embedded images by <img src>.
    """
