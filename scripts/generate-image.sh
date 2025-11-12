#!/bin/bash

# Image Generation Helper Script
# Usage: ./scripts/generate-image.sh "your prompt here" output-name

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Load environment variables
if [ -f .env ]; then
    source .env
else
    echo -e "${RED}❌ .env file not found. Copy .env.example to .env and add your API keys${NC}"
    exit 1
fi

# Check for required arguments
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 \"prompt text\" output-name"
    echo "Example: $0 \"Professional plumber fixing leak\" plumber-leak-repair"
    exit 1
fi

PROMPT="$1"
OUTPUT_NAME="$2"
TEMP_FILE="/tmp/${OUTPUT_NAME}.png"

echo -e "${BLUE}🎨 Generating image with DALL·E 3...${NC}"
echo "Prompt: $PROMPT"

# Generate image with DALL·E 3
response=$(curl -s -X POST https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"dall-e-3\",
    \"prompt\": \"$PROMPT\",
    \"n\": 1,
    \"size\": \"1792x1024\",
    \"quality\": \"hd\"
  }")

# Check for errors
if echo "$response" | grep -q "error"; then
    echo -e "${RED}❌ Error generating image:${NC}"
    echo "$response" | jq '.error'
    exit 1
fi

# Extract image URL
image_url=$(echo "$response" | jq -r '.data[0].url')

if [ -z "$image_url" ] || [ "$image_url" == "null" ]; then
    echo -e "${RED}❌ Failed to get image URL${NC}"
    echo "$response"
    exit 1
fi

echo -e "${GREEN}✓ Image generated successfully${NC}"
echo "URL: $image_url"

# Download image
echo -e "${BLUE}📥 Downloading image...${NC}"
curl -s -o "$TEMP_FILE" "$image_url"

if [ ! -f "$TEMP_FILE" ]; then
    echo -e "${RED}❌ Failed to download image${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Downloaded to $TEMP_FILE${NC}"

# Convert to WebP (multiple sizes)
echo -e "${BLUE}🔄 Converting to WebP...${NC}"

# 420w (mobile/cards)
cwebp -q 85 -m 6 -resize 420 0 "$TEMP_FILE" \
  -o "img/${OUTPUT_NAME}-420w.webp"
size_420=$(du -h "img/${OUTPUT_NAME}-420w.webp" | cut -f1)

# 800w (desktop/medium)
cwebp -q 85 -m 6 -resize 800 0 "$TEMP_FILE" \
  -o "img/${OUTPUT_NAME}-800w.webp"
size_800=$(du -h "img/${OUTPUT_NAME}-800w.webp" | cut -f1)

# 1200w (hero/large) - optional
cwebp -q 85 -m 6 -resize 1200 0 "$TEMP_FILE" \
  -o "img/${OUTPUT_NAME}-1200w.webp"
size_1200=$(du -h "img/${OUTPUT_NAME}-1200w.webp" | cut -f1)

echo -e "${GREEN}✓ WebP conversion complete${NC}"
echo "  - img/${OUTPUT_NAME}-420w.webp ($size_420)"
echo "  - img/${OUTPUT_NAME}-800w.webp ($size_800)"
echo "  - img/${OUTPUT_NAME}-1200w.webp ($size_1200)"

# Clean up
rm "$TEMP_FILE"

# Generate HTML snippet
echo ""
echo -e "${BLUE}📝 HTML Implementation:${NC}"
cat <<EOF

<!-- For service cards -->
<picture>
    <source type="image/webp"
            srcset="img/${OUTPUT_NAME}-420w.webp 420w, img/${OUTPUT_NAME}-800w.webp 800w"
            sizes="(max-width: 768px) 100vw, 420px">
    <img src="img/${OUTPUT_NAME}-420w.webp"
         alt="TODO: Add descriptive alt text"
         width="420" height="420"
         loading="lazy" decoding="async">
</picture>

<!-- For hero sections -->
<picture>
    <source type="image/webp"
            srcset="img/${OUTPUT_NAME}-800w.webp 800w,
                    img/${OUTPUT_NAME}-1200w.webp 1200w"
            sizes="(max-width: 768px) 100vw, 1200px">
    <img src="img/${OUTPUT_NAME}-800w.webp"
         alt="TODO: Add descriptive alt text"
         loading="eager" decoding="async">
</picture>

EOF

echo -e "${GREEN}✅ Done! Images ready to use.${NC}"
