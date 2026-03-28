import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface Props {
  labels: string[];
  opened: number[];
  closed: number[];
}

export default function PRsChart({ labels, opened, closed }: Props) {
  if (!labels.length) {
    return <div style={{ background: "#fff", borderRadius: 12, padding: 20, flex: 1 }}>Carregando...</div>;
  }

  return (
    <div style={{ background: "#fff", borderRadius: 12, padding: 20, flex: 1, minWidth: 300 }}>
      <Line
        data={{
          labels,
          datasets: [
            { label: "Abertos", data: opened, borderColor: "#f59e0b", tension: 0.3 },
            { label: "Fechados", data: closed, borderColor: "#10b981", tension: 0.3 },
          ],
        }}
        options={{
          responsive: true,
          plugins: { title: { display: true, text: "PRs Abertos vs Fechados" } },
        }}
      />
    </div>
  );
}
