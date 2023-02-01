import React, { useEffect } from "react";
import { createGlobalStyle } from "styled-components";
import PropTypes from "prop-types";
import Table from "./Table";
import moment from "moment";
import { Icon } from "@iconify/react";
import PopoverBox from "../ui/Popover";
import { DayPicker } from "react-day-picker";
import { useRouter } from "next/router";

function Events({ tableData }) {
  const router = useRouter();

  const [startDates, setStartDate] = React.useState();
  const [endDates, setEndDate] = React.useState();

  const [dates, setDate] = React.useState([]);

  useEffect(() => {
    let startDate = new Date();

    const endDate = new Date(startDate).setDate(startDate.getDate() + 7);
    const allDates = [];

    if (startDates && endDates) {
      var currentDate = moment(startDates);
      var stopDate = moment(endDates);
      while (currentDate <= stopDate) {
        allDates.push(moment(currentDate).format("YYYY-MM-DD"));
        currentDate = moment(currentDate).add(1, "days");
      }
    } else {
      while (startDate <= endDate) {
        allDates.push(new Date(startDate));
        startDate.setDate(startDate.getDate() + 1);
      }
    }

    setDate(allDates);
  }, [startDates, endDates]);

  const columns = React.useMemo(
    () => [
      {
        Header: tableData.name,
        Cell: (row) => {
          return tableData.rooms[row.row.index].name;
        },
      },
      ...dates.map((date) => {
        return {
          Header: moment(date).format("MMM Do"),
          Cell: (row) => {
            const room = tableData.rooms[row.row.index];
            const dateData = room.room_availabilities.find((roomDate) => {
              return (
                moment(roomDate.date).format("YYYY-MM-DD") ===
                moment(date).format("YYYY-MM-DD")
              );
            });

            return (
              <>
                {dateData && (
                  <div className="flex flex-col">
                    <div className="text-xs font-bold text-gray-600">
                      ${dateData.price}
                    </div>
                    <div className="text-xs text-gray-600">
                      {dateData.num_of_available_rooms} Available
                    </div>
                  </div>
                )}

                {!dateData && (
                  <div className="text-xs text-gray-600">
                    <h1 className="font-black"> -- </h1>
                  </div>
                )}
              </>
            );
          },
        };
      }),
    ],
    [dates]
  );

  const GlobalStyle = createGlobalStyle`
  .rdp-cell {
    width: 50px !important;
    height: 50px !important;
    border-radius: 100px !important;
  }
  rdp-day {
    border-radius: 100px !important;
  }
  .rdp-months {
    width: 100% !important;
  }
  .rdp-day_range_middle {
    opacity: 0.5 !important;
  }

  .hsds-beacon .eTCLra {
    @media (max-width: 768px) {
      bottom: 70px !important;
    }
  }

    table {
      border-spacing: 0;


      tr {
        :last-child {
          td {
            border-bottom: 0;
          }
        }
      }

      th,
      td {
        margin: 4;
        padding: 0.5rem;

        :last-child {
          border-right: 0;
        }
      }
    }
  `;

  const data = React.useMemo(() => tableData.rooms, [tableData]);
  return (
    <div className="px-2 h-screen overflow-x-scroll">
      <GlobalStyle></GlobalStyle>

      {data.length > 0 && (
        <div className="flex items-center gap-4 mb-6 justify-center">
          <PopoverBox
            panelClassName="bg-white rounded-xl shadow-md mt-2 border w-[400px] p-2"
            btnPopover={
              <div className="w-[220px] px-2 py-2 flex items-center cursor-pointer justify-between text-sm text-gray-500 h-[35px] border border-gray-300">
                {!startDates && <h1>Arrival date</h1>}
                {startDates && (
                  <h1>{moment(startDates).format("MMM Do YYYY")}</h1>
                )}
                <Icon
                  className="w-6 h-6 text-gray-700"
                  icon="clarity:date-solid"
                />
              </div>
            }
          >
            <DayPicker
              mode="single"
              disabled={{ before: new Date() }}
              selected={startDates}
              onSelect={(date) => {
                setStartDate(date);
                setEndDate(null);
              }}
            />
          </PopoverBox>

          <div className="w-[20px] h-[1px] bg-gray-500"></div>
          <PopoverBox
            panelClassName="bg-white rounded-xl shadow-md mt-2 border w-[400px] p-2"
            btnPopover={
              <div className="w-[220px] px-2 py-2 flex items-center cursor-pointer justify-between text-sm text-gray-500 h-[35px] border border-gray-300">
                {!endDates && <h1>Depature date</h1>}
                {endDates && <h1>{moment(endDates).format("MMM Do YYYY")}</h1>}
                <Icon
                  className="w-6 h-6 text-gray-700"
                  icon="clarity:date-solid"
                />
              </div>
            }
          >
            <DayPicker
              mode="single"
              disabled={{ before: new Date() }}
              selected={endDates}
              onSelect={(date) => {
                setEndDate(date);
              }}
            />
          </PopoverBox>
        </div>
      )}

      <div className="w-full">
        {data.length > 0 && <Table columns={columns} data={data}></Table>}
      </div>

      {data.length === 0 && (
        <div className="h-full flex-col gap-2 flex items-center justify-center">
          <Icon
            className="w-[40px] h-[40px] text-gray-500"
            icon="mdi:house-city"
          />
          <h1 className="text-xl font-bold text-gray-500">No data</h1>
        </div>
      )}
    </div>
  );
}

Events.propTypes = {};

export default Events;
