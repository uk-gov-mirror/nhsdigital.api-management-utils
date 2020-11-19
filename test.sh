t="one,two,three"
template_files=($(echo "$t" | tr ',' '\n'))
for template_file in "${template_files[@]}"; do
    echo $template_file
done