import React from "react";
import PropTypes from "prop-types";
import moment from "moment";
import Table from "./Table";
import { createGlobalStyle } from "styled-components";
import { useFormik } from "formik";
import * as Yup from "yup";
import Dialogue from "../Home/Dialogue";
import Input from "../ui/Input";
import PopoverBox from "../ui/Popover";
import { DayPicker } from "react-day-picker";
import "react-day-picker/dist/style.css";
import { Icon } from "@iconify/react";
import axios from "axios";
import LoadingSpinerChase from "../ui/LoadingSpinerChase";
import Cookies from "js-cookie";

function RoomAvailability({
  availability,
  roomName,
  roomSlug,
  setOpenAddAvailabilityModal,
  setRoomAvailabilities,
}) {
  const roomAvailability = React.useMemo(() => availability, [availability]);

  const [deleteAvailabilityLoading, setDeleteAvailabilityLoading] =
    React.useState(false);

  const [editAvailabilityLoading, setEditAvailabilityLoading] =
    React.useState(false);

  const [openEditAvailabilityModal, setOpenEditAvailabilityModal] =
    React.useState(false);

  const formikEdit = useFormik({
    initialValues: {
      number_of_available_rooms: "",
      price: "",
      date: "",
      rowSlug: "",
    },
    validationSchema: Yup.object({
      number_of_available_rooms: Yup.number().required(
        "Number of available rooms is required"
      ),
      price: Yup.number().required("Price is required"),
      date: Yup.date().required("Date is required"),
    }),
    onSubmit: (values) => {
      setEditAvailabilityLoading(true);
      axios
        .put(
          `${process.env.NEXT_PUBLIC_baseURL}/room-types/${roomSlug}/availabilities/${values.rowSlug}/`,
          {
            num_of_available_rooms: values.number_of_available_rooms,
            price: values.price,
            date: moment(values.date).format("YYYY-MM-DD"),
          },
          {
            headers: {
              Authorization: "Token " + Cookies.get("token"),
            },
          }
        )
        .then((res) => {
          setRoomAvailabilities(
            roomAvailability.map((item) => {
              if (item.slug === values.rowSlug) {
                return {
                  ...item,
                  num_of_available_rooms: values.number_of_available_rooms,
                  price: values.price,
                  date: moment(values.date).format("YYYY-MM-DD"),
                };
              }
              return item;
            })
          );
          setEditAvailabilityLoading(false);
          setOpenEditAvailabilityModal(false);
        })
        .catch((err) => {
          setEditAvailabilityLoading(false);
        });
    },
  });

  const columns = React.useMemo(
    () => [
      {
        Header: "#",
        Cell: (row) => {
          return row.row.index + 1;
        },
      },
      {
        Header: "Date",
        accessor: "date",
        Cell: (row) => {
          return (
            <h1 className="font-bold">
              {moment(row.row.original.date).format("MMM Do")}
            </h1>
          );
        },
      },
      {
        Header: "Available Rooms",
        accessor: "num_of_available_rooms",
        Cell: (row) => {
          return row.row.original.num_of_available_rooms;
        },
      },
      {
        Header: "Price",
        accessor: "price",
        Cell: (row) => {
          return "$" + row.row.original.price;
        },
      },
      {
        Header: "Actions",
        Cell: (row) => {
          return (
            <div className="flex gap-2">
              <button
                onClick={() => {
                  editAvailability(row.row.original);
                }}
                className="bg-blue-500 text-white px-2 py-1 rounded-md"
              >
                Edit
              </button>
              <button
                onClick={() => {
                  deleteAvailability(row.row.original);
                }}
                className="bg-red-500 flex items-center justify-center gap-1 text-white px-2 py-1 rounded-md"
              >
                Delete{" "}
                {deleteAvailabilityLoading && (
                  <div>
                    <LoadingSpinerChase
                      color="white"
                      width={12}
                      height={12}
                    ></LoadingSpinerChase>
                  </div>
                )}
              </button>
            </div>
          );
        },
      },
    ],
    [roomAvailability]
  );

  const editAvailability = (row) => {
    formikEdit.setFieldValue(
      "number_of_available_rooms",
      row.num_of_available_rooms
    );
    formikEdit.setFieldValue("price", row.price);
    formikEdit.setFieldValue("date", row.date);
    formikEdit.setFieldValue("rowSlug", row.slug);
    setOpenEditAvailabilityModal(true);
  };

  const deleteAvailability = (row) => {
    axios
      .delete(
        `${process.env.NEXT_PUBLIC_baseURL}/room-types/${roomSlug}/availabilities/${row.slug}/`,
        {
          headers: {
            Authorization: "Token " + Cookies.get("token"),
          },
        }
      )
      .then((res) => {
        setRoomAvailabilities(
          roomAvailability.filter((item) => item.slug !== row.slug)
        );
      })
      .catch((err) => {});
  };

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

  return (
    <div className="w-full">
      <GlobalStyle></GlobalStyle>
      {roomAvailability.length > 0 && (
        <Table columns={columns} data={roomAvailability}></Table>
      )}

      {roomAvailability.length === 0 && (
        <div className="flex flex-col p-6 items-center justify-center h-full">
          <h1 className="text-base font-bold">No Availability added yet</h1>
          <button
            onClick={() => {
              setOpenAddAvailabilityModal(true);
            }}
            className="bg-blue-500 text-white mt-2 px-6 py-0.5 rounded-md"
          >
            Add
          </button>
        </div>
      )}

      <Dialogue
        isOpen={openEditAvailabilityModal}
        closeModal={() => {
          setOpenEditAvailabilityModal(false);
        }}
        dialogueTitleClassName="!font-bold !ml-4 !text-xl md:!text-2xl"
        outsideDialogueClass="!p-0"
        dialoguePanelClassName={
          "md:!rounded-md !rounded-none !p-0 overflow-y-scroll remove-scroll !max-w-lg screen-height-safari md:!min-h-0 md:max-h-[500px] "
        }
      >
        <div className="px-4 py-2">
          <h1 className="font-bold font-SourceSans text-lg truncate">
            <span className="text-gray-600">Add availability to </span>
            {roomName}
          </h1>

          <div className="mt-4 flex gap-3 flex-col">
            <div className="flex flex-col gap-1">
              <h1 className="text-sm font-bold">
                What date is the room available?
              </h1>
              <PopoverBox
                panelClassName="bg-white rounded-xl shadow-md mt-2 border w-[400px] p-2"
                btnClassName="w-full"
                btnPopover={
                  <div
                    className={
                      "!w-full rounded-md px-2 py-5 flex items-center cursor-pointer justify-between text-sm text-gray-500 h-[35px] border border-gray-300 " +
                      (formikEdit.touched.date && formikEdit.errors.date
                        ? "border-red-500"
                        : "")
                    }
                  >
                    {!formikEdit.values.date && (
                      <h1 className="font-bold text-gray-400">
                        Availability date
                      </h1>
                    )}
                    {formikEdit.values.date && (
                      <h1>
                        {moment(formikEdit.values.date).format("MMM Do YYYY")}
                      </h1>
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
                  selected={formikEdit.values.date}
                  onSelect={(date) => {
                    formikEdit.setFieldValue("date", date);
                  }}
                />
              </PopoverBox>

              {formikEdit.touched.date && formikEdit.errors.date ? (
                <span className="text-sm font-bold text-red-400">
                  {formikEdit.errors.date}
                </span>
              ) : null}
            </div>

            <div>
              <Input
                name="number_of_available_rooms"
                type="number"
                value={formikEdit.values.number_of_available_rooms}
                placeholder="Number of available rooms"
                errorStyle={
                  formikEdit.touched.number_of_available_rooms &&
                  formikEdit.errors.number_of_available_rooms
                    ? true
                    : false
                }
                onChange={(e) => {
                  formikEdit.handleChange(e);
                }}
                className={"w-full placeholder:text-sm "}
                inputClassName="!text-sm "
                label="Add the number of rooms that is available on the selected date"
              ></Input>
              {formikEdit.touched.number_of_available_rooms &&
              formikEdit.errors.number_of_available_rooms ? (
                <span className="text-sm font-bold text-red-400">
                  {formikEdit.errors.number_of_available_rooms}
                </span>
              ) : null}
            </div>

            <div>
              <Input
                name="price"
                type="number"
                value={formikEdit.values.price}
                placeholder="Price on selected date"
                errorStyle={
                  formikEdit.touched.price && formikEdit.errors.price
                    ? true
                    : false
                }
                onChange={(e) => {
                  formikEdit.handleChange(e);
                }}
                className={"w-full placeholder:text-sm "}
                inputClassName="!text-sm "
                label="Add the price of the room on the selected date"
              ></Input>
              {formikEdit.touched.price && formikEdit.errors.price ? (
                <span className="text-sm font-bold text-red-400">
                  {formikEdit.errors.price}
                </span>
              ) : null}
            </div>
          </div>

          <div className="flex items-center gap-4 mt-6">
            <button
              onClick={() => {
                setOpenEditAvailabilityModal(false);
              }}
              className="bg-gray-200 w-[40%] text-sm font-bold px-6 py-2 rounded-md"
            >
              Cancel
            </button>
            <button
              onClick={() => {
                formikEdit.handleSubmit();
              }}
              className="bg-blue-500 w-[60%] flex items-center justify-center gap-1 text-white font-bold px-2 py-1.5 rounded-md"
            >
              Edit{" "}
              {editAvailabilityLoading && (
                <div>
                  <LoadingSpinerChase
                    color="white"
                    width={12}
                    height={12}
                  ></LoadingSpinerChase>
                </div>
              )}
            </button>
          </div>
        </div>
      </Dialogue>
    </div>
  );
}

RoomAvailability.propTypes = {};

export default RoomAvailability;
