import React from "react";
import PropTypes from "prop-types";
import Link from "next/link";
import Image from "next/image";
import { Icon } from "@iconify/react";
import getToken from "../../../lib/getToken";
import axios from "axios";
import { useRouter } from "next/router";

import Calendar from "../../../components/Partner/Calendar";
import Events from "../../../components/Partner/Events";
import Analytics from "../../../components/Partner/Analytics";
import SelectOptions from "../../../components/Partner/SelectOptions";
import Accommodation from "../../../components/Partner/Accommodation";

function PartnerLodges({ stays }) {
  const router = useRouter();

  const tableData = {
    id: 1,
    name: "Mara Serena Lodge",

    rooms: [
      {
        id: 1,
        name: "Standard Room",
        dates: [
          {
            id: 1,
            price: 100,
            available: 2,
            date: "2023-02-01",
          },
          {
            id: 2,
            price: 130,
            available: 1,
            date: "2023-02-02",
          },
          {
            id: 3,
            price: 150,
            available: 0,
            date: "2023-02-03",
          },
          {
            id: 4,
            price: 120,
            available: 1,
            date: "2023-02-04",
          },
          {
            id: 5,
            price: 100,
            available: 2,
            date: "2023-02-06",
          },
        ],
      },
      {
        id: 2,
        name: "Deluxe Room",

        dates: [
          {
            id: 1,
            price: 100,
            available: 2,
            date: "2023-02-01",
          },
          {
            id: 2,
            price: 130,
            available: 1,
            date: "2023-02-02",
          },
          {
            id: 3,
            price: 150,
            available: 0,
            date: "2023-02-03",
          },
          {
            id: 4,
            price: 120,
            available: 1,
            date: "2023-02-04",
          },
          {
            id: 5,
            price: 100,
            available: 2,
            date: "2023-02-05",
          },
        ],
      },
      {
        id: 3,
        name: "Family Room",

        dates: [
          {
            id: 1,
            price: 100,
            available: 2,
            date: "2023-02-01",
          },
          {
            id: 2,
            price: 130,
            available: 1,
            date: "2023-02-02",
          },
          {
            id: 3,
            price: 150,
            available: 0,
            date: "2023-02-03",
          },
          {
            id: 4,
            price: 120,
            available: 1,
            date: "2023-02-04",
          },
          {
            id: 5,
            price: 100,
            available: 2,
            date: "2023-02-05",
          },
        ],
      },
    ],
  };

  return (
    <div className="flex">
      <div className="w-[350px]">
        <div className="px-3 py-2 h-[70px] border-b flex items-center justify-center">
          <div className="flex gap-4 items-center justify-center">
            <div className="relative w-28 h-9 z-40">
              <Image
                layout="fill"
                alt="Logo"
                src="/images/winda_logo/horizontal-blue-font.png"
                priority
              ></Image>
            </div>

            <div className="h-[25px] w-[1px] mt-4 z-40 bg-gray-400"></div>

            <h1 className="uppercase font-OpenSans mt-3 text-lg text-gray-700 tracking-widest z-40">
              partner
            </h1>
          </div>
        </div>

        <h1 className="mt-4 font-bold ml-3 text-xl font-SourceSans">
          Your Accommodation
        </h1>

        <div className="px-4 mt-5 relative flex flex-col gap-5">
          {stays.map((stay, index) => (
            <Accommodation
              listing={stay}
              key={index}
              index={index}
            ></Accommodation>
          ))}
        </div>
      </div>

      <div className="flex-grow px-4 border-l relative flex flex-col gap-6 overflow-x-scroll pt-8">
        <Events
          tableData={{
            name:
              stays.length > 0
                ? stays[router.query.index ? Number(router.query.index) : 0]
                    .property_name ||
                  stays[router.query.index ? Number(router.query.index) : 0]
                    .name
                : "",
            rooms:
              stays.length > 0
                ? stays[router.query.index ? Number(router.query.index) : 0]
                    .room_types
                : [],
          }}
        ></Events>
      </div>
    </div>
  );
}

PartnerLodges.propTypes = {};

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
      const stays = await axios.get(
        `${process.env.NEXT_PUBLIC_baseURL}/user-stays/`,
        {
          headers: {
            Authorization: "Token " + token,
          },
        }
      );

      return {
        props: {
          userProfile: response.data[0],
          stays: stays.data.results,
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
          destination: `/login?redirect=/partner/lodges`,
        },
      };
    } else {
      return {
        props: {
          userProfile: "",
          stays: [],
        },
      };
    }
  }
}

export default PartnerLodges;
