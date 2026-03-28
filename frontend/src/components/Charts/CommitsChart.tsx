import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface Props {
  labels: string[];
  data: number[];
}

export default function CommitsChart({ labels, data }: Props) {
  if (!labels.length) {
    return <div style={{ background: "#fff", borderRadius: 12, padding: 20, flex: 1 }}>Carregando...</div>;
  }

  return (
    <div style={{ background: "#fff", borderRadius: 12, padding: 20, flex: 1, minWidth: 300 }}>
      <Bar
        data={{
          labels,
          datasets: [{
            label: "Commits/semana",
            data,
            backgroundColor: "rgba(6, 182, 212, 0.7)",
            borderRadius: 6,
          }],
        }}
        options={{
          responsive: true,
          plugins: { legend: { display: false }, title: { display: true, text: "Commits por Semana" } },
        }}
      />
    </div>
  );
}
