# bot/handlers/view.py

from telegram import Update
from telegram.ext import ContextTypes

async def ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    article = context.user_data.get("article")
    if not article:
        await update.message.reply_text("❌ No hay artículo cargado para ver.")
        return

    preview = f"""📝 <b>Artículo actual</b>

<b>Título:</b> {article['title']}
<b>Subtítulo:</b> {article['excerpt']}
<b>Slug:</b> {article['slug']}
<b>Categoría:</b> {article['categories'][0] if article['categories'] else 'Sin clasificar'}
<b>Etiquetas:</b> {", ".join(article['tags'])}
<b>SEO keywords:</b> {", ".join(article['seo']['keywords'])}

<b>Cuerpo:</b>
{article['body'][:1000]}{"..." if len(article['body']) > 1000 else ""}
"""

    await update.message.reply_text(preview, parse_mode="HTML")
