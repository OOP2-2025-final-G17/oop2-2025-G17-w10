// static/js/radar_chart.js

document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("radarChart");
  if (!canvas) return; // シフトがない場合

  const labels = JSON.parse(canvas.dataset.labels);
  const values = JSON.parse(canvas.dataset.values);

  new Chart(canvas, {
    type: "radar",
    data: {
      labels: labels,
      datasets: [{
        label: "職場ごとの人数",
        data: values,
        fill: true
      }]
    },
    options: {
      scales: {
        r: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          }
        }
      }
    }
  });
});
