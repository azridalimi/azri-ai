
import os
import gradio as gr
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

ARAHAN = """
Nama kamu ialah HazeShield AI.

Kamu ialah pembantu AI untuk projek HazeShield yang memfokuskan
kepada kesihatan tanaman, jerebu, kualiti udara, pencemaran udara,
dan teknologi pertanian pintar.

Kamu boleh membantu berkaitan pelbagai jenis tanaman seperti:
sayur-sayuran, buah-buahan, tanaman hiasan, pokok dan tanaman
pertanian lain. Jangan hadkan jawapan kepada padi sahaja.

Jawab dalam Bahasa Melayu yang jelas, mesra dan mudah difahami.
Terangkan bagaimana jerebu dan pencemaran udara boleh mempengaruhi
fotosintesis, pertumbuhan, daun dan kesihatan tanaman.

Bantu pengguna memahami pemantauan kualiti udara, sensor,
Internet of Things (IoT), rumah hijau dan kaedah perlindungan tanaman.

Jangan mereka-reka bacaan sensor, data saintifik atau fakta.
Bezakan fakta yang diketahui daripada cadangan atau anggaran.
Berikan langkah penjagaan tanaman yang praktikal dan selamat.
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

Soalan pengguna:
{mesej}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        jawapan = response.text or "Maaf, tiada jawapan diterima."
    except Exception as e:
        print("Ralat Gemini:", repr(e))
        jawapan = (
            "Maaf, HazeShield AI menghadapi masalah sementara. "
            "Sila cuba lagi sebentar."
        )

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

with gr.Blocks(title="HazeShield AI") as demo:
    memori = gr.State([])

    with gr.Row():
        with gr.Column(scale=1, min_width=200):
            gr.Markdown("# 🌿 HazeShield AI")
            butang_baru = gr.Button("＋ Perbualan Baharu")
            gr.Markdown("---")
            gr.Markdown(
                "Pembantu AI untuk kesihatan tanaman, "
                "jerebu dan pertanian pintar."
            )

        with gr.Column(scale=4):
            gr.Markdown("# 🌱 HazeShield AI")
            gr.Markdown(
                "Tanya tentang jerebu, kualiti udara dan kesihatan tanaman."
            )

            ruang_chat = gr.Chatbot(
                label="Perbualan",
                height=450
            )

            mesej = gr.Textbox(
                placeholder="Contoh: Bagaimana jerebu menjejaskan tanaman?",
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
