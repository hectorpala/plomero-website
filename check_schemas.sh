#!/bin/bash
echo "=== Estado de Schemas por Servicio ==="
echo
for dir in servicios/*/; do
    if [ -f "$dir/index.html" ]; then
        name=$(basename "$dir")
        service=$(grep -c '"@type": "Service"' "$dir/index.html" 2>/dev/null || echo 0)
        faq=$(grep -c '"@type": "FAQPage"' "$dir/index.html" 2>/dev/null || echo 0)
        
        if [ "$service" -gt 0 ] && [ "$faq" -gt 0 ]; then
            echo "✅ $name - Service + FAQPage"
        elif [ "$service" -gt 0 ]; then
            echo "⚠️  $name - Solo Service"
        elif [ "$faq" -gt 0 ]; then
            echo "⚠️  $name - Solo FAQPage"
        else
            echo "❌ $name - Sin schemas"
        fi
    fi
done
