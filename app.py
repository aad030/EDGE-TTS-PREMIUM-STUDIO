import gradio as gr

# Custom CSS for Premium Look
custom_css = """
body { background-color: #0a0e17 !important; }
.gradio-container { border: 2px solid #c5a059 !important; border-radius: 15px !important; }
.gr-box { background: rgba(20, 25, 40, 0.8) !important; border: 1px solid #334466 !important; }
button { background: linear-gradient(135deg, #444, #111) !important; color: white !important; border: 1px solid #c5a059 !important; border-radius: 8px !important; }
.compile-btn { background: linear-gradient(135deg, #2b5876, #4e4376) !important; color: white !important; font-weight: bold !important; }
"""

def generate_audio(voice, speed, pitch):
    # Yahan tumhara backend logic aayega (jo audio generate karega)
    return "Audio Processed Successfully!"

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# <div style='text-align: center; color: #c5a059;'>Voice Settings</div>")
    
    with gr.Column(elem_classes="gr-box"):
        voice_dropdown = gr.Dropdown(choices=["Asad (Urdu) PK"], label="Select Voice")
        speed_slider = gr.Slider(minimum=-10, maximum=10, value=0, label="Speed (%)")
        pitch_slider = gr.Slider(minimum=-10, maximum=10, value=0, label="Pitch (Hz)")
    
    compile_btn = gr.Button("COMPILE AUDIO ASSETS", elem_classes="compile-btn")
    
    with gr.Row():
        gr.Button("Studio")
        gr.Button("Privacy")
        gr.Button("Terms")
        gr.Button("Contact")

    compile_btn.click(fn=generate_audio, inputs=[voice_dropdown, speed_slider, pitch_slider])

demo.launch()
