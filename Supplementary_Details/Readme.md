# Diffusion Illusions: Supplementary Projects

This folder contains implementations of various visual illusions using Stable Diffusion. The code is organized into separate Jupyter Notebooks for each effect.

## 0. Interactive Demo Website

We have prepared an interactive website to easily view the generated results (tangram, cylinder, anamorphic).

**How to run:**

1. Install Streamlit:
   `pip install streamlit`

2. Run the script from the project root directory:
   `streamlit run Generate_Website.py`

- **Note on File Paths:**
   Ensure you are in the root directory of the project (the folder containing `Generate_Website.py`) when running the command. The script uses relative paths to locate images and demos in the `Supplementary_Details` folder. If you see "File not found" errors, please check your current working directory, or change the corresponding paths in the python file.

## 1. Installation

The installation commands are embedded within each notebook.

- **Environment**:
  - For **Kaleidoscope,  Cylinder, and Anamorphic** illusions, usage of **Google Colab** or **Kaggle** with GPU support (e.g., Tesla P100) is recommended.
  - For **Tangram and Image Prompt illusions**, usage of **AutoDL** with GPU support is recommended.
- **Dependencies**: The initial cells in each notebook handle dependency installation and repository cloning.
- **Important**: **Restart the Runtime/Session** after the initial installation step to avoid library conflicts.

## 2. Kaleidoscope Illusion

**Notebook**: `Kaleidoscope.ipynb`

1. **Setup**: Run the `Setup Environment` cell to install dependencies. **Restart the session** immediately after this step.
2. **Configuration**: The notebook is pre-configured with a "Four Seasons" story (Spring, Summer, Autumn, Winter) corresponding to 0°, 90°, 180°, and 270° rotations. You can modify the `prompts` list to create your own story.
3. **Training**: Run the following cells sequentially to the main loop. Then Run the `Main Optimization Loop` cell. The code optimizes the image to satisfy specific text prompts at different rotation angles. It takes just less than 3 hours on Kaggle GPU T4 * 2.
4. **Visualization**: Run the final cell to generate and display a GIF animation (`kaleidoscope_seasons.gif`) showing the rotation effect.

## 3. Cylindrical Illusion

**Notebook**: `cylinder.ipynb`

1. **Setup**: Switch the runtime to **GPU**. Run the top 2 cells to install `numpy` and clone the necessary repository.
2. **Restart**: **Restart the Runtime**. This is crucial for fixing dependency versions.
3. **Run**: Execute the remaining cells sequentially.
    - **Concept**: This generates a "Cylindrical Anamorphosis" where a distorted flat image reveals a coherent 3D object when reflected on a central cylinder.
    - **Customization**: You can edit `prompt_flat` for the rug/mat pattern and `prompt_cylinder` for the object inside the reflection.
4. **Output**: The script visualizes the optimization process and saves the final clear flat pattern as `cylinder_illusion_flat.png`.
5. **Visualization**: You can use the `create_Cylinder_demo` provided in the `create_demo_code` folder, change the png name inside the code, and run it to see the gif effect.(In our case, a gif in `demos` folder is offered for reference.)

## 4. Anamorphic Illusion

**Notebook**: `anamorphic_illusion.ipynb`

1. **Setup**: Choose a GPU accelerator. Run the first cell block to set up the environment.
2. **Restart**: **Restart the cells/session** as instructed in the output.
3. **Run**: Run the rest of the cells sequentially.
    - **View A (Top-down)**: Defined by `prompt_flat` (e.g., "A distinct texture of wood").
    - **View B (Perspective)**: Defined by `prompt_perspective` (e.g., "A standing 3D coca-cola can"), visible only from a specific grazing angle.
4. **Result**: The notebook displays the "Flat" view side-by-side with the "Perspective" illusion view during training and saves the final results.
5. **Visualization**: Use the `create_Anamorphic_demo` in the `create_demo_code` folder, change the png name inside the code, and run it to see the gif effect. (A reference gif is provided in the `demos` folder.)

## 5. Tangram

**Notebook**:

- Original: `tangram_original.ipynb`
- Image Prompt: `tangram_image_prompt.ipynb`
- Learnable Layout: `learnable_tangram.ipynb`

1. **Setup**: Choose a GPU accelerator. Run the first cell block to set up the environment.
2. **Restart**: **Restart the cells/session** as instructed in the output.
3. **Run**: Run the rest of the cells sequentially.
   - **Customization**: You can edit `ARR_A` and `ARR_B` to modify the arrangements of tangram pieces.
      - For image prompts, use `load_ref_image` to load custom images.
      - For learnable layout tangram, modify `LAMBDA_OVERLAP` to punish overlapping.
4. **Result**: The notebook displays two views alongside prime image during the training process.
5. **Visualization**: Run `generate_gif.py` to generate timelapses(you need to save notebook results previously). Remember to save the picture into a folder and name the folder `images`.You can tweak `start_duration` and `end_duration` to create acceleration effects.

## 6. CLIP Score Evaluation

**Script**: `clip_score.py`

- 需要人工调整clip_score.py中的data_samples列表，填入需要评估的生成图路径及对应的text prompt和image prompt路径。
- 运行后，会输出每张图的CLIP-Text Score和CLIP-Image Score，并计算平均分数。
- 运行指令: `python clip_score.py`
