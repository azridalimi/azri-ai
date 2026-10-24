
import os
import gradio as gr
from google import genai

# API key akan ditetapkan secara rahsia dalam Render
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

ARAHAN = """
Kamu ialah Azri AI, pembantu AI yang mesra.
Jawab dalam Bahasa Melayu yang mudah difahami.
Bantu pengguna belajar pengaturcaraan langkah demi langkah.
Gunakan sejarah perbualan untuk menjawab soalan susulan.
"""

def balas_mesej(mesej, memori, paparan_chat):
    if not mesej or not mesej.strip():
        return paparan_chat or [], memori or [], ""

    memori = memori or []
    paparan_chat = paparan_chat or []

    sejarah = ""
    for item in memori:
        sejarah += f"{item['role']}: {item['content']}\n"

    prompt = f"""
{ARAHAN}

Sejarah perbualan:
{sejarah}

Soalan terkini pengguna:
{mesej}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        jawapan = response.text or "Maaf, tiada jawapan diterima."
    except Exception:
        jawapan = "Maaf, Azri AI menghadapi masalah. Cuba lagi sebentar."

    memori_baru = memori + [
        {"role": "user", "content": mesej},
        {"role": "assistant", "content": jawapan}
    ]

    paparan_baru = paparan_chat + [
        {"role": "user", "content": mesej},
        {"role": "assistant", "content": jawapan}
    ]

    return paparan_baru, memori_baru, ""

def chat_baharu():
    return [], [], ""

with gr.Blocks(title="Azri AI") as demo:
    memori = gr.State([])

    with gr.Row():
        with gr.Column(scale=1, min_width=200):
            gr.Markdown("# ✨ Azri AI")
            butang_baru = gr.Button("＋ Chat Baharu")
            gr.Markdown("---")
            gr.Markdown("Pembantu AI peribadi anda.")

        with gr.Column(scale=4):
            gr.Markdown("# Azri AI")
            ruang_chat = gr.Chatbot(
                label="Perbualan",
                height=450
            )
            mesej = gr.Textbox(
                placeholder="Tanya sesuatu kepada Azri AI...",
                label="Mesej",
                lines=2
            )
            hantar = gr.Button("Hantar", variant="primary")

    inputs_chat = [mesej, memori, ruang_chat]
    outputs_chat = [ruang_chat, memori, mesej]

    hantar.click(
        balas_mesej,
        inputs=inputs_chat,
        outputs=outputs_chat
    )

    mesej.submit(
        balas_mesej,
        inputs=inputs_chat,
        outputs=outputs_chat
    )

    butang_baru.click(
        chat_baharu,
        inputs=[],
        outputs=[ruang_chat, memori, mesej]
    )

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
