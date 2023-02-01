import React from "react";
import PropTypes from "prop-types";
import LineChart from "./LineChart";
import { Icon } from "@iconify/react";
import moment from "moment/moment";

import SwiperCore, { Navigation, Pagination } from "swiper";
import { Swiper, SwiperSlide } from "swiper/react";
SwiperCore.use([Navigation]);

import "swiper/css";
import "swiper/css/navigation";

function Analytics({ trips }) {
  const settings = {
    spaceBetween: 10,
    slidesPerView: "auto",
    pagination: {
      dynamicBullets: true,
    },
  };

  const totalEarnedWithinTheLastThirtyDays = () => {
    let total = 0;
    trips.forEach((trip) => {
      if (
        trip.date >= moment().subtract(30, "days").format("YYYY-MM-DD") &&
        trip.date < moment().add(1, "days").format("YYYY-MM-DD")
      ) {
        total += trip.amount_paid;
      }
    });
    return total;
  };

  const totalEarnedBeforeLastThirtyDays = () => {
    let total = 0;
    trips.forEach((trip) => {
      if (trip.date < moment().subtract(30, "days").format("YYYY-MM-DD")) {
        total += trip.amount_paid;
      }
    });
    return total;
  };

  const percentChange = () => {
    const percentChange =
      ((totalEarnedWithinTheLastThirtyDays() -
        totalEarnedBeforeLastThirtyDays()) /
        totalEarnedWithinTheLastThirtyDays()) *
      100;
    return percentChange;
  };

  const totalTripsWithinTheLastThirtyDays = () => {
    let total = 0;
    trips.forEach((trip) => {
      if (
        trip.date >= moment().subtract(30, "days").format("YYYY-MM-DD") &&
        trip.date < moment().add(1, "days").format("YYYY-MM-DD")
      ) {
        total += 1;
      }
    });
    return total;
  };

  const totalTripsBeforeLastThirtyDays = () => {
    let total = 0;
    trips.forEach((trip) => {
      if (trip.date < moment().subtract(30, "days").format("YYYY-MM-DD")) {
        total += 1;
      }
    });
    return total;
  };

  const percentChangeTrips = () => {
    const percentChangeTrips =
      ((totalTripsWithinTheLastThirtyDays() -
        totalTripsBeforeLastThirtyDays()) /
        totalTripsWithinTheLastThirtyDays()) *
      100;
    return percentChangeTrips;
  };

  const totalPassengersWithinTheLastThirtyDays = () => {
    let total = 0;
    trips.forEach((trip) => {
      if (
        trip.date >= moment().subtract(30, "days").format("YYYY-MM-DD") &&
        trip.date < moment().add(1, "days").format("YYYY-MM-DD")
      ) {
        total += trip.number_of_guests;
      }
    });
    return total;
  };

  const totalPassengersBeforeLastThirtyDays = () => {
    let total = 0;
    trips.forEach((trip) => {
      if (trip.date < moment().subtract(30, "days").format("YYYY-MM-DD")) {
        total += trip.number_of_guests;
      }
    });
    return total;
  };

  const percentChangePassengers = () => {
    const percentChangePassengers =
      ((totalPassengersWithinTheLastThirtyDays() -
        totalPassengersBeforeLastThirtyDays()) /
        totalPassengersWithinTheLastThirtyDays()) *
      100;
    return percentChangePassengers;
  };

  return (
    <div className="w-full">
      <div className="px-3">
        <h1 className="mb-6 mt-4 text-2xl font-black">Insights & Analytics</h1>

        <Swiper
          {...settings}
          modules={[Navigation, Pagination]}
          navigation
          className="!h-full !w-full !relative "
        >
          <SwiperSlide className="px-4 !w-[300px] py-2 rounded-lg border bg-white">
            <div className="flex justify-between items-center">
              <div className="bg-blue-600 w-10 h-10 rounded-md bg-opacity-30 flex items-center justify-center">
                <Icon className="w-5 h-5" icon="ph:currency-dollar-bold" />
              </div>

              <div className="flex items-center gap-0.5">
                <Icon
                  className="text-blue-600"
                  icon="material-symbols:arrow-outward"
                />
                <h1 className="text-blue-600 text-sm font-bold">
                  {Math.round(percentChange())}%
                </h1>
                <div className="text-gray-500 text-sm"> | </div>
                <h1 className="text-gray-500 text-sm">Last 30 days</h1>
              </div>
            </div>

            <div className="mt-4 flex flex-col gap-1">
              <h1 className="font-black text-lg">
                KES{totalEarnedWithinTheLastThirtyDays().toLocaleString()}
              </h1>
              <h1 className="text-gray-500 text-sm">
                Total Earnings within the last 30 days
              </h1>
            </div>
          </SwiperSlide>

          <SwiperSlide className="px-4 !w-[300px] py-2 rounded-lg border bg-white">
            <div className="flex justify-between items-center">
              <div className="bg-blue-600 w-10 h-10 rounded-md bg-opacity-30 flex items-center justify-center">
                <Icon className="w-6 h-6" icon="bx:trip" />
              </div>

              <div className="flex items-center gap-0.5">
                <Icon
                  className="text-blue-600"
                  icon="material-symbols:arrow-outward"
                />
                <h1 className="text-blue-600 text-sm font-bold">
                  {Math.round(Math.round(percentChangeTrips()))}%
                </h1>
                <div className="text-gray-500 text-sm"> | </div>
                <h1 className="text-gray-500 text-sm">Last 30 days</h1>
              </div>
            </div>

            <div className="mt-4 flex flex-col gap-1">
              <h1 className="font-black text-lg">
                {totalTripsWithinTheLastThirtyDays().toLocaleString()} trips
              </h1>
              <h1 className="text-gray-500 text-sm">Within the last 30 days</h1>
            </div>
          </SwiperSlide>

          <SwiperSlide className="px-4 !w-[300px] py-2 rounded-lg border bg-white">
            <div className="flex justify-between items-center">
              <div className="bg-blue-600 w-10 h-10 rounded-md bg-opacity-30 flex items-center justify-center">
                <Icon className="w-6 h-6" icon="ph:user-circle-bold" />
              </div>

              <div className="flex items-center gap-0.5">
                <Icon
                  className="text-blue-600"
                  icon="material-symbols:arrow-outward"
                />
                <h1 className="text-blue-600 text-sm font-bold">
                  {Math.round(percentChangePassengers())}%
                </h1>
                <div className="text-gray-500 text-sm"> | </div>
                <h1 className="text-gray-500 text-sm">Last 30 days</h1>
              </div>
            </div>

            <div className="mt-4 flex flex-col gap-1">
              <h1 className="font-black text-lg">
                {totalPassengersWithinTheLastThirtyDays()} passengers
              </h1>
              <h1 className="text-gray-500 text-sm">Within the last 30 days</h1>
            </div>
          </SwiperSlide>
        </Swiper>
      </div>

      <div className="max-w-4xl mt-8">
        <LineChart trips={trips}></LineChart>
      </div>
    </div>
  );
}

Analytics.propTypes = {};

export default Analytics;
