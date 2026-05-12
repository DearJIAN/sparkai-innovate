import sys, os, time
sys.path.insert(0, '.')
from app import create_app
app = create_app()

with app.app_context():
    from models.material_evaluation import MaterialEvaluation
    from services.material_report_pdf import generate_report_pdf

    ev = MaterialEvaluation.query.get(8)
    output_dir = r"E:\LEAR-CODE-NEW\软件工程\my-keshe\innovation-competition-platform\backend\uploads\material_evaluation\reports"

    print("Starting PDF generation...")
    t0 = time.time()
    path = generate_report_pdf(ev, output_dir)
    t1 = time.time()
    print(f"PDF generated in {t1-t0:.2f}s")
    print(f"Path: {path}")
    print(f"Size: {os.path.getsize(path)} bytes")