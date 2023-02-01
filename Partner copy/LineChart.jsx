import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import moment from "moment";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: "top",
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: "Date",
      },
      grid: {
        display: false,
      },
      ticks: {
        font: {
          size: 10,
        },
        autoSkip: true,
      },
    },
  },
};

const getAllDatesBetweenTwoDates = (startDate, endDate) => {
  let allDates = [];
  let currentDate = startDate;

  while (currentDate <= endDate) {
    // push only odd dates
    if (currentDate.getDate() % 2 !== 0) {
      allDates.push(moment(currentDate).format("MMM D"));
    } else {
      allDates.push("");
    }
    // allDates.push(moment(currentDate).format("Do MMM, YY"));
    // add one day to current date
    currentDate = new Date(currentDate.setDate(currentDate.getDate() + 1));
  }
  return allDates;
};
const currentDate = new Date();
const thirtyDaysBeforeCurrentDate = new Date(
  currentDate.setDate(currentDate.getDate() - 30)
);

const dates = getAllDatesBetweenTwoDates(
  thirtyDaysBeforeCurrentDate,
  new Date()
);

function LineChart({ trips }) {
  const getPriceOfDateInTrip = (date) => {
    let price = 0;
    trips.forEach((trip) => {
      if (trip.date === moment(date).format("YYYY-MM-DD")) {
        price += trip.amount_paid;
      }
    });
    return price;
  };

  const getAllPricesBetweenTwoDates = (startDate, endDate) => {
    let allPrices = [];
    let currentDate = startDate;

    while (currentDate <= endDate) {
      allPrices.push(getPriceOfDateInTrip(currentDate));
      currentDate = new Date(currentDate.setDate(currentDate.getDate() + 1));
    }
    return allPrices;
  };

  const date = new Date();
  const thirtyDaysBefore = new Date(date.setDate(date.getDate() - 30));

  let prices = getAllPricesBetweenTwoDates(
    new Date(new Date().setDate(new Date().getDate() - 30)),
    new Date()
  );

  const data = {
    labels: dates,
    datasets: [
      {
        label: "Price",
        data: prices,
        borderColor: "rgb(53, 162, 235)",
        backgroundColor: "rgba(53, 162, 235, 0.5)",
      },
    ],
  };

  return <Line options={options} data={data} />;
}

export default LineChart;
