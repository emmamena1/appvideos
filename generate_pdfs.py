import os
from fpdf import FPDF

def create_bonus_pdf(markdown_path, image_path, output_path):
    # Initialize PDF with explicit A4 dimensions
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # 1. Portada
    pdf.add_page()
    if os.path.exists(image_path):
        # Image filling most of the page, centered
        pdf.image(image_path, x=20, y=20, w=170)
    
    # 2. Contenido
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    
    if os.path.exists(markdown_path):
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    pdf.ln(5)
                    continue
                
                # Clean text for FPDF latin-1 compatibility
                clean_line = line.encode('latin-1', 'replace').decode('latin-1')
                
                if line.startswith('# '):
                    pdf.set_font("helvetica", "B", 20)
                    pdf.multi_cell(170, 10, clean_line[2:])
                    pdf.ln(5)
                elif line.startswith('## '):
                    pdf.set_font("helvetica", "B", 16)
                    pdf.multi_cell(170, 10, clean_line[3:])
                    pdf.ln(3)
                elif line.startswith('### '):
                    pdf.set_font("helvetica", "B", 14)
                    pdf.multi_cell(170, 10, clean_line[4:])
                    pdf.ln(2)
                else:
                    pdf.set_font("helvetica", size=12)
                    pdf.multi_cell(170, 7, clean_line)
                    pdf.ln(1)
    
    pdf.output(output_path)
    print(f"✅ Generado: {output_path}")

if __name__ == "__main__":
    base_dir = r"c:\Users\Emmanuel\Desktop\appvideos"
    bonos_dir = os.path.join(base_dir, "bonos_frutiferas")
    output_dir = os.path.join(base_dir, "bonos_pdf_final")
    mockups_dir = r"C:\Users\Emmanuel\.gemini\antigravity\brain\6924fa54-5bfb-45d1-9b8d-7f6fc70eb100"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = [
        ("bono_1_riego_y_abono.md", "mockup_bono_riego_y_abono_1768133171438.png", "Bono_1_Calendario_Riego.pdf"),
        ("bono_2_antiplagas_organicas.md", "mockup_bono_antiplagas_1768133464179.png", "Bono_2_Guia_Antiplagas.pdf"),
        ("bono_3_lista_compras.md", "mockup_bono_lista_compras_1768133479158.png", "Bono_3_Lista_Compras.pdf"),
        ("bono_4_frutas_principiantes.md", "mockup_bono_frutas_principiantes_1768133493244.png", "Bono_4_Top_Frutas.pdf"),
    ]

    for md, img, out in files:
        create_bonus_pdf(
            os.path.join(bonos_dir, md),
            os.path.join(mockups_dir, img),
            os.path.join(output_dir, out)
        )
