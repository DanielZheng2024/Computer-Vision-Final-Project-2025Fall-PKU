import torch
import clip
from PIL import Image
import pandas as pd
from tqdm import tqdm
import os
# --- 配置区 ---
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "ViT-L/14"  # 12GB 显存建议用这个标准模型
BATCH_SIZE = 32

# 数据样例：每个生成图路径对应其 text prompt 和 image prompt 路径
data_samples = [
    {
        "gen_img": "outputs/ims_0029_part1.png", 
        "text_prompt": "a red fox, ultra detailed", 
        "ref_img": ""
    },
    {
        "gen_img": "outputs/ims_0029_part2.png", 
        "text_prompt": "a blue robot, cinematic lighting", 
        "ref_img": ""
    },
    {
        "gen_img": "outputs/imgp1.png", 
        "text_prompt": "a red fox, ultra detailed", 
        "ref_img": "ref_image/2.jpg"
    },
    {
        "gen_img": "outputs/imgp2.png", 
        "text_prompt": "", 
        "ref_img": "ref_image/3.jpg"
    },
    {
        "gen_img": "outputs/ims_0039_part1.png", 
        "text_prompt": "", 
        "ref_img": "ref_image/2.jpg"
    },
    {
        "gen_img": "outputs/ims_0039_part2.png", 
        "text_prompt": "", 
        "ref_img": "ref_image/3.jpg"
    },
]

# --------------

def batch_evaluate():
    # 加载模型
    model, preprocess = clip.load(MODEL_NAME, device=DEVICE)
    results = []

    # 使用 tqdm 显示进度
    for i in tqdm(range(0, len(data_samples), BATCH_SIZE)):
        batch = data_samples[i : i + BATCH_SIZE]
        
        gen_images = []
        texts = []
        ref_images = []
        ref_indices = [] # 记录哪些样本拥有参考图
        
        # 1. 预处理数据
        for idx, item in enumerate(batch):
            # 处理生成图和文本（假设这些肯定存在）
            gen_images.append(preprocess(Image.open(item["gen_img"])))
            texts.append(clip.tokenize(item["text_prompt"]))
            
            # 处理参考图（可能不存在）
            if item.get("ref_img") and os.path.exists(item["ref_img"]):
                ref_images.append(preprocess(Image.open(item["ref_img"])))
                ref_indices.append(idx) # 记录该参考图对应 Batch 中的第几个样本

        # 转换为 Tensor 并推送到设备
        gen_input = torch.stack(gen_images).to(DEVICE)
        text_input = torch.cat(texts).to(DEVICE)
        
        with torch.no_grad():
            # 提取并归一化特征
            gen_feat = model.encode_image(gen_input)
            gen_feat /= gen_feat.norm(dim=-1, keepdim=True)
            
            text_feat = model.encode_text(text_input)
            text_feat /= text_feat.norm(dim=-1, keepdim=True)

            # --- 计算 Text Score ---
            # 直接按位相乘并求和 (batch_size, dims) -> (batch_size)
            text_scores = (gen_feat * text_feat).sum(dim=-1) * 100
            
            # --- 计算 Image Score (安全处理) ---
            img_scores = [None] * len(batch)
            if ref_images:
                ref_input = torch.stack(ref_images).to(DEVICE)
                ref_feat = model.encode_image(ref_input)
                ref_feat /= ref_feat.norm(dim=-1, keepdim=True)
                
                # 只计算存在参考图的样本
                # 我们提取出对应的 gen_feat 进行比对
                matched_gen_feat = gen_feat[ref_indices] 
                matched_scores = (matched_gen_feat * ref_feat).sum(dim=-1) * 100
                
                # 将结果填回对应位置
                for sub_idx, original_idx in enumerate(ref_indices):
                    img_scores[original_idx] = float(matched_scores[sub_idx])

        # 3. 收集结果
        for idx, item in enumerate(batch):
            results.append({
                "file": item["gen_img"],
                "clip_text_score": float(text_scores[idx]),
                "clip_img_score": img_scores[idx] if img_scores[idx] is not None else "N/A"
            })

    # 保存报告
    df = pd.DataFrame(results)
    df.to_csv("evaluation_report.csv", index=False)
    
    # 打印统计信息
    avg_text = df["clip_text_score"].mean()
    print(f"\nProcessing Complete!")
    print(f"Average CLIP-Text Score: {avg_text:.2f}")
    
    # 如果有图片分数，打印图片分数的平均值
    valid_img_scores = df[df["clip_img_score"] != "N/A"]["clip_img_score"]
    if not valid_img_scores.empty:
        print(f"Average CLIP-Image Score: {valid_img_scores.astype(float).mean():.2f}")

if __name__ == "__main__":
    # 请确保在此之前你已经填充了 data_samples 列表
    if not data_samples:
        print("Error: data_samples is empty. Please populate it with your image paths.")
    else:
        batch_evaluate()