import os
import sys
import torch

# Shap-E imports
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh

def main():
    # 1. Parse command-line argument
    if len(sys.argv) < 2:
        print("Usage: python3 modeling.py \"Your prompt here\"")
        sys.exit(1)

    prompt = sys.argv[1]

    # 2. Device selection (GPU if available, else CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # 3. Load models
    print("Loading models...")
    xm = load_model("transmitter", device=device)
    model = load_model("text300M", device=device)
    diffusion = diffusion_from_config(load_config("diffusion"))

    # 4. Generate latents from the prompt
    print(f"Generating latents for prompt: {prompt}")
    batch_size = 1
    guidance_scale = 15.0

    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(texts=[prompt] * batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=64,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )

    # 5. Set base directory for output files
    base_dir = os.path.join(os.getcwd(), "static")
    os.makedirs(base_dir, exist_ok=True)  # Ensure the directory exists

    print("Decoding latents to meshes and saving files...")
    for i, latent in enumerate(latents):
        # Decode latent into a triangle mesh
        tri_mesh = decode_latent_mesh(xm, latent).tri_mesh()

        # Write to .ply
        ply_filename = os.path.join(base_dir, f"generated_model_{i}.ply")
        with open(ply_filename, "wb") as f_ply:
            tri_mesh.write_ply(f_ply)

        # Write to .obj
        obj_filename = os.path.join(base_dir, f"generated_model_{i}.obj")
        with open(obj_filename, "w") as f_obj:
            tri_mesh.write_obj(f_obj)

        print(f"Saved mesh {i} as '{ply_filename}' and '{obj_filename}'")

    print("Done!")

if __name__ == "__main__":
    main()
