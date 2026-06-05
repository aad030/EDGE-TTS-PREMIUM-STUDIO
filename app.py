import gradio as gr

# Premium CSS for that metallic/glassmorphism look
custom_css = """
body {
    background-color: #0a0e17;
    background-image: radial-gradient(circle at 70% 30%, #1a2a40 0%, #0a0e17 70%);
}
.gradio-container {
    border: 2px solid #c5a059;
    border-radius: 15px;
    padding: 20px;
}
/* Styling the main containers */
.gr-box {
    background: rgba(20, 25, 40, 0.8) !important;
    border: 1px solid #334466 !important;
    border-radius: 10px !important;
}
/* Metallic Gradient Buttons */
button {
    background: linear-gradient(135deg, #444, #111) !important;
    color: white !important;
    border: 1px solid #c5a059 !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}
/* Highlighted 'Compile' Button */
.compile-btn {
    background: linear-gradient(135deg, #2b5876, #4e4376) !important;
    box-shadow: 0 0 15px rgba(78, 67, 118, 0.6) !important;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# <div style='text-align: center; color: #c5a059;'>Voice Settings</div>")
    
    with gr.Column(elem_classes="gr-box"):
        voice_dropdown = gr.Dropdown(choices=["Asad (Urdu) PK"], label="Select Voice")
        speed_slider = gr.Slider(minimum=-10, maximum=10, label="Speed")
        pitch_slider = gr.Slider(minimum=-10, maximum=10, label="Pitch")
    
    compile_btn = gr.Button("COMPILE & SYNTHESIZE AUDIO", elem_classes="compile-btn")
    
    with gr.Row():
        gr.Button("Studio")
        gr.Button("Privacy")
        gr.Button("Terms")
        gr.Button("Contact")

demo.launch()
