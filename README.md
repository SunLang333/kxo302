# KXO302 — AR Home Decorator

A full-stack project that generates 3D models from text and lets you place them in your room in AR.

## What it does

1. **Generate** — enter a text prompt in the web app; the backend runs OpenAI's [Shap-E](https://github.com/openai/shap-e) on PyTorch and produces a 3D model (.ply).
2. **View** — preview the generated models in the browser (space builder and viewer pages).
3. **Decorate in AR** — open the model in the Meta Quest 3 app: set up your space, select a model, then move and rearrange it freely in the room.

## Demo

Web — text-to-3D generation:

[![Demo 1](https://github.com/SunLang333/kxo302/blob/main/kxo302demo1.gif?raw=true)](https://github.com/SunLang333/kxo302/raw/refs/heads/main/kxo302demo1.mp4)

Quest 3 — AR placement (space setup, model selection, free rearrangement):

[![Demo 2](https://github.com/SunLang333/kxo302/blob/main/kxo302demo2.gif?raw=true)](https://github.com/SunLang333/kxo302/raw/refs/heads/main/kxo302demo2.mp4)

## Tech stack

- **Backend:** Python + Flask; model generation via Shap-E / PyTorch, invoked from the `/generate` route as a subprocess
- **Frontend:** HTML / CSS / JavaScript with Jinja templates
- **AR client:** Meta Quest 3

## Run the web app

```bash
pip install -r requirements.txt
python main.py
```

Then open http://localhost:5000.

| Route | Page |
|---|---|
| `/` | Home |
| `/products` | Product list |
| `/spacebuilder` | Generate a model from a text prompt and preview it |
| `/viewer` | Model viewer |
| `/generate` (POST) | Runs Shap-E with the submitted prompt |
| `/download` | Download page |
