---
name: japanese-magazine-cover
description: Create a Japanese-style magazine cover from an uploaded portrait by generating a separate transparent overlay and compositing it onto the untouched original.
---

# Japanese Magazine Cover

Use this skill when the user wants an editorial Japanese magazine cover made from a portrait photograph and the photograph must remain unchanged.

## Core invariant

The uploaded portrait is the base layer and is never sent to an image editor as the thing to repaint. Generate cover typography, borders, labels, and decorative graphics as a separate PNG with a real alpha channel. The final image is a deterministic alpha composite of the original and that overlay. Keep the original file and the transparent overlay as separate deliverables.

## Workflow

1. Identify the portrait file and the requested cover copy, language, mood, colors, and output orientation. Inspect the portrait with `view_image` when composition or subject placement matters.
2. Use the built-in `image_gen` tool to generate the cover overlay. Treat the portrait as a layout/reference image only. Ask for:
   - a genuinely transparent background and preserved alpha;
   - the exact pixel dimensions or aspect ratio of the portrait;
   - Japanese editorial typography, masthead, captions, rules, stickers, and other requested graphics;
   - no person, face, body, skin, hair, photographic background, or replacement pixels;
   - no opaque full-frame wash unless the user explicitly requests one;
   - clear space over important facial features and readable text.
   Quote required text verbatim. If the generated asset is not transparent, has the wrong dimensions, or contains regenerated photographic content, regenerate the overlay rather than compositing it.
3. Save or copy the generated PNG into the working folder as `cover-overlay.png`. Do not overwrite an existing asset without the user's explicit request.
4. Composite with the included deterministic helper:

   ```bash
   python scripts/compose_cover.py \
     --original /path/to/portrait.jpg \
     --overlay /path/to/cover-overlay.png \
     --output /path/to/japanese-magazine-cover.jpg
   ```

   The helper resizes the overlay exactly to the original canvas when dimensions differ, preserves the original canvas and pixels as the base, and writes a JPEG when the output path ends in `.jpg` or `.jpeg` (use PNG only when an alpha-preserving flattened output is explicitly needed). It refuses an overlay without alpha and reports the input dimensions and SHA-256 hash.
5. Inspect the composite. If placement is wrong, change the overlay and rerun the compositor; never repair the result by editing the flattened composite. Return links to the untouched original, the transparent overlay, and the final composite when they are available.

## Design quality control

Treat the cover as an edited publication layout, not a collection of decorations. Keep one clear masthead, one main headline, and at most three secondary information groups. Leave deliberate breathing room; do not fill every empty area. Use one dominant accent color plus one supporting accent, and limit badges, stickers, arrows, doodles, and barcode elements to only those that support the theme.

Every text block must be readable against the local photograph at full size and in a thumbnail preview. Do not place text over faces, skin, clothing details, balloons, cake, bright highlights, dense branches, or similarly colored/high-frequency areas. Choose text colors by local contrast rather than by a fixed palette. When a text block must cross a detailed photo area, use a small local solid or translucent backing shape, a restrained outline, or a subtle shadow behind that block; never use a full-frame wash. Remove any text or decoration that is low-contrast, crowded, redundant, or too small to read.

## 完整封面蒙版提示词

生成蒙版时，使用下面这段完整提示词，并在末尾保留“只输出透明蒙版”的约束：

```text
把这张原照片设计成一张高完成度、日本时尚杂志风格的专业封面。

首先分析原照片的内容、人物、场景、服装、色彩、氛围和视觉重点，根据照片本身自动判断最合适的杂志主题、标题风格、配色和排版方式。不要预设季节、地点、人物关系或具体主题；所有文字和视觉元素都应根据照片内容生成。

最重要：
严格保留原照片中的人物和主体，不要改变人物的脸。
保持原人物的五官、脸型、表情、发型、肤色、年龄感、身份特征、姿势、动作、身体比例和服装。
不要重新生成、重绘、美化或替换人物脸部。
保持原照片的真实摄影感。

尽可能保留原始照片的构图、环境、光线和主体，只在其基础上增加专业杂志封面设计。

整体风格：
高级日本时尚杂志、生活方式杂志、青年杂志的真实出版物质感。
现代、时髦、精致、有设计感，但不要过度商业化，也不要像普通宣传海报。

加入丰富且自然的杂志视觉元素，例如：
大型 Masthead / Magazine Logo、醒目的主标题、副标题、多组栏目标题、日文与英文混排、手写字体、圆形徽章、贴纸、标签、线条、箭头、涂鸦、日期、期号、价格、条形码、SPECIAL ISSUE / FEATURE / EDITORIAL 等杂志信息、根据照片主题生成的小型装饰元素。

根据照片内容自动生成合适的文案。
例如人物照片可以偏向 fashion / lifestyle / youth；旅行照片可以偏向 travel / culture；城市照片可以偏向 architecture / city life；食物照片可以偏向 food / gourmet；自然风景可以偏向 nature / travel；产品照片可以偏向 design / lifestyle；但不要局限于这些分类，应根据照片实际内容自由判断。

文字不要全部使用单一的黑白字体。
根据原照片的颜色和氛围自动选择协调的强调色，并使用不同字体大小、字重、方向和排版方式形成明显的视觉层级。

可以加入条形码、日期、价格、期号、圆形标章、贴纸、限定信息等真实杂志元素，让封面信息丰富但保持高级感。

排版必须根据原照片的构图自适应，并遵守专业杂志的留白与可读性：
不要固定套用模板；
优先利用天空、墙面、道路、留白区域等自然空间；
不要遮挡人物的脸和主体；
不要破坏原照片最重要的视觉焦点；
只保留一个主 Masthead、一个主标题和不超过三组副信息；
不要把文字、贴纸、徽章、箭头和条形码堆满画面，保留明确留白；
文字必须与所在区域形成清晰明度和色彩对比，避开与背景相近的颜色；
如果照片局部细节太复杂，只在对应文字块后加入小范围底色、描边或阴影，不使用整幅半透明色罩；
合成后检查全尺寸和缩略图，删除低对比度、重复、拥挤或不可读的元素。

最终效果应该像一本真正发行的日本时尚 / 生活方式杂志封面，而不是一张普通图片加文字。

这是透明封面蒙版生成任务：只生成文字、图形、装饰和杂志信息，不要生成或重绘任何照片像素。输出必须是带真实 alpha 通道的透明 PNG，尺寸和原照片一致；透明区域保持透明。不要输出完整照片，不要添加不透明全屏背景、照片滤镜、色彩覆盖或水印。最终设计要克制、留白明确、层级清楚、文字对比度足够，像经过编辑和印刷审核的真实杂志封面。
```

使用这段提示词时，仍然把上传照片作为布局参考和最终合成的底图，不要把它作为需要重绘的编辑目标。

## Prompt template for the overlay

```text
Use case: ads-marketing
Asset type: transparent editorial magazine-cover overlay
Input image: portrait photo used only as a layout/reference image; do not repaint or include any photo pixels
Primary request: create a Japanese fashion/lifestyle magazine cover overlay at exactly <WIDTH>x<HEIGHT>
Text (verbatim): "<MASTHEAD>" and "<COVER LINES>"
Composition/framing: keep the face and subject unobstructed; place typography and accents in the available negative space
Style/medium: refined Japanese editorial typography, print-like rules and small labels
Constraints: transparent background with alpha; typography and graphic elements only; no person, face, skin, hair, body, scenery, opaque background, watermark, or altered photographic content
Avoid: regenerated portrait pixels, blur or color grading applied to the photo, illegible or invented text
```

For exact copy that image generation cannot render reliably, create the text as a separate transparent text layer with a local font and composite it using the same helper. The non-negotiable requirement is that every photographic pixel comes from the original input.
