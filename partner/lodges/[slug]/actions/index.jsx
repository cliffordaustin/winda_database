import React from "react";
import PropTypes from "prop-types";
import getToken from "../../../../../lib/getToken";
import axios from "axios";
import { Icon } from "@iconify/react";
import { useRouter } from "next/router";
import RoomTypes from "../../../../../components/Partner/RoomTypes";
import PopoverBox from "../../../../../components/ui/Popover";
import { useFormik } from "formik";
import * as Yup from "yup";
import Input from "../../../../../components/ui/Input";
import { Popover, Transition } from "@headlessui/react";
import LoadingSpinerChase from "../../../../../components/ui/LoadingSpinerChase";
import Cookies from "js-cookie";

function AddAvailability({ stay }) {
  const router = useRouter();
  const [createRoomLoading, setCreateRoomLoading] = React.useState(false);

  const formikCreate = useFormik({
    initialValues: {
      name: "",
    },
    validationSchema: Yup.object({
      name: Yup.string().required("Please enter a name for the room"),
    }),
    onSubmit: (values) => {
      setCreateRoomLoading(true);
      axios
        .post(
          `${process.env.NEXT_PUBLIC_baseURL}/stays/${router.query.slug}/add-room-type/`,
          {
            name: values.name,
          },
          {
            headers: {
              Authorization: "Token " + Cookies.get("token"),
            },
          }
        )
        .then((res) => {
          router.reload();
        })
        .catch((err) => {
          setCreateRoomLoading(false);
        });
    },
  });

  return (
    <div>
      <div className="max-w-[1100px] mt-6 mx-auto px-6 xl:px-0">
        <div
          onClick={() => {
            router.back();
          }}
          className="flex gap-1 mb-3 font-bold cursor-pointer items-center text-blue-600"
        >
          <Icon className="w-6 h-6" icon="bx:chevron-left" />
          <span>Back</span>
        </div>
        <div className="flex items-center justify-between">
          <h1 className="font-bold font-SourceSans text-2xl truncate">
            <span className="text-gray-600">Add/edit</span>{" "}
            {stay.property_name || stay.name}{" "}
            <span className="text-gray-600">availability</span>
          </h1>

          <Popover className="relative ">
            <Popover.Button className="outline-none ">
              <button
                onClick={() => {}}
                className="bg-blue-500 text-white text-sm font-bold mt-2 px-6 py-1.5 rounded-md"
              >
                Add a room
              </button>
            </Popover.Button>

            <Transition
              as={React.Fragment}
              enter="transition ease-out duration-200"
              enterFrom="opacity-0 translate-y-1"
              enterTo="opacity-100 translate-y-0"
              leave="transition ease-in duration-150"
              leaveFrom="opacity-100 translate-y-0"
              leaveTo="opacity-0 translate-y-1"
            >
              <Popover.Panel
                className={
                  "absolute z-[30] bg-white rounded-xl !right-0 shadow-md mt-2 border w-[400px] px-3 py-3"
                }
              >
                <div>
                  <Input
                    name="name"
                    type="text"
                    value={formikCreate.values.name}
                    placeholder="Enter the name of the room. eg. Standard Room"
                    errorStyle={
                      formikCreate.touched.name && formikCreate.errors.name
                        ? true
                        : false
                    }
                    onChange={(e) => {
                      formikCreate.handleChange(e);
                    }}
                    className={"w-full placeholder:text-sm "}
                    inputClassName="!text-sm "
                    label="Room name"
                  ></Input>
                  {formikCreate.touched.name && formikCreate.errors.name ? (
                    <span className="text-sm font-bold text-red-400">
                      {formikCreate.errors.name}
                    </span>
                  ) : null}
                </div>

                <div className="flex justify-end mt-4">
                  <Popover.Button className="bg-gray-200 text-sm font-bold px-6 py-1.5 rounded-md">
                    Cancel
                  </Popover.Button>

                  <button
                    onClick={() => {
                      formikCreate.handleSubmit();
                    }}
                    className="bg-blue-500 flex justify-center items-center gap-2 text-white text-sm font-bold ml-2 px-6 py-1.5 rounded-md"
                  >
                    Post{" "}
                    {createRoomLoading && (
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
              </Popover.Panel>
            </Transition>
          </Popover>
        </div>

        <div className="flex-col flex gap-4 mt-10">
          {stay.room_types.map((room, index) => (
            <RoomTypes key={index} room={room} index={index}></RoomTypes>
          ))}
        </div>
      </div>
    </div>
  );
}

AddAvailability.propTypes = {};

export async function getServerSideProps(context) {
  try {
    const token = getToken(context);

    const response = await axios.get(
      `${process.env.NEXT_PUBLIC_baseURL}/user/`,
      {
        headers: {
          Authorization: "Token " + token,
        },
      }
    );

    if (response.data[0].is_partner) {
      const stay = await axios.get(
        `${process.env.NEXT_PUBLIC_baseURL}/user-stays/${context.params.slug}`,
        {
          headers: {
            Authorization: "Token " + token,
          },
        }
      );

      return {
        props: {
          userProfile: response.data[0],
          stay: stay.data,
        },
      };
    } else {
      return {
        notFound: true,
      };
    }
  } catch (error) {
    if (error.response.status === 401) {
      return {
        redirect: {
          permanent: false,
          destination: `/login?redirect=/partner/lodges/${context.params.slug}/edit`,
        },
      };
    } else {
      return {
        props: {
          userProfile: "",
          stay: [],
        },
      };
    }
  }
}

export default AddAvailability;
