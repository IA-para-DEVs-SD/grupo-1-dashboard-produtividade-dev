import csv
import io
from datetime import datetime

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from src.services.metrics import MetricsService

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/csv")
async def export_csv(
    from_date: str | None = Query(None, alias="from"),
    to_date: str | None = Query(None, alias="to"),
):
    svc = MetricsService()
    data = await svc.calculate(from_date, to_date)

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["metrica", "valor"])
    for key, val in data.items():
        writer.writerow([key, val])
    buf.seek(0)

    filename = f"metricas_{datetime.now():%Y%m%d}.csv"
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/pdf")
async def export_pdf(
    from_date: str | None = Query(None, alias="from"),
    to_date: str | None = Query(None, alias="to"),
):
    from fpdf import FPDF

    svc = MetricsService()
    data = await svc.calculate(from_date, to_date)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Dashboard Produtividade Dev", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Gerado em {datetime.now():%Y-%m-%d %H:%M}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(95, 8, "Metrica", border=1)
    pdf.cell(95, 8, "Valor", border=1, ln=True)
    pdf.set_font("Helvetica", "", 11)
    for key, val in data.items():
        pdf.cell(95, 8, str(key), border=1)
        pdf.cell(95, 8, str(val), border=1, ln=True)

    buf = io.BytesIO(pdf.output())
    filename = f"relatorio_{datetime.now():%Y%m%d}.pdf"
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
