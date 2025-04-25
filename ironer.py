import xml.etree.ElementTree as ET

# Cargar el XML con soporte para estructuras más complejas
def load_data_from_xml(xml_file):
    tree = ET.parse(xml_file)  
    root = tree.getroot()
    data = {}

    for child in root:
        if len(child):
            if all(grandchild.tag == child[0].tag for grandchild in child):
                data[child.tag] = [{subchild.tag: subchild.text for subchild in grandchild} for grandchild in child]
            else:
                data[child.tag] = {subchild.tag: subchild.text for subchild in child}
        else:
            data[child.tag] = child.text
    
    # Extraer imágenes de ODS y sectores (solo las especificadas en XML)
    data["ODS"] = [value for key, value in data.items() if key.startswith("ODS")]
    data["Sectores"] = [value for key, value in data.items() if key.startswith("sector")]
    
    return data

# Cargar el template HTML y reemplazar campos
def render_template(template_path, output_path, data):
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Reemplazo de valores estándar
    for key, value in data.items():
        if isinstance(value, list):
            value = ', '.join(str(item) for item in value)
        elif isinstance(value, dict):
            value = ', '.join(f'{k}: {v}' for k, v in value.items())
        html = html.replace(f'###{key}###', value)

    # Reemplazo de imágenes de ODS
    ods_images = ''.join(f'<img src="Original/ODS/{img}" class="img-fluid m-2" style="max-width: 70px;">' for img in data.get("ODS", []))
    html = html.replace("###ods_images###", ods_images)

    # Reemplazo de imágenes de sectores
    sector_images = ''.join(f'<img src="Original/Sectores/{img}" class="img-fluid m-2" style="max-width: 70px;">' for img in data.get("Sectores", []))
    html = html.replace("###sector_images###", sector_images)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

# Archivos
xml_file = 'plantillaproyectos1.xml'
template_file = 'template.html'
output_file = 'output.html'

# Datos adicionales
additional_data = {
    "titulo": "Agua potable en la población Baka de Camerún",
    "logos": [{"path": "logo1.png"}, {"path": "logo2.png"}]
}

# Ejecutar
data = load_data_from_xml(xml_file)
data.update(additional_data)
render_template(template_file, output_file, data)
