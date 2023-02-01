import React from "react";
import PropTypes from "prop-types";
import Carousel from "../ui/Carousel";
import Image from "next/image";
import Button from "../ui/Button";
import { Icon } from "@iconify/react";
import PopoverBox from "../ui/Popover";
import Link from "next/link";
import { useRouter } from "next/router";

function Accommodation({ listing, index }) {
  const sortedImages = listing.stay_images.sort((x, y) => y.main - x.main);
  const router = useRouter();

  const images = sortedImages.map((image) => {
    return image.image;
  });

  const selectedIndex = Number(router.query.index) || 0;

  return (
    <div
      className={
        "w-full flex xl:flex-row rounded-md flex-col " +
        (selectedIndex === index ? "border border-blue-600" : "border-none")
      }
    >
      <div className={"w-[240px] h-[150px] relative"}>
        <Image
          className={"w-full object-cover "}
          src={images[0]}
          alt=""
          objectPosition="center"
          layout="fill"
        />
      </div>

      <div className="xl:px-2 xl:py-2 flex flex-col xl:justify-between">
        <div className="flex flex-col gap-0.5 mt-2 xl:mt-0">
          <h1 className="uppercase text-gray-500 text-xs">
            {listing.location}
          </h1>
          <h1 className="font-bold font-SourceSans text-xl truncate">
            {listing.property_name || listing.name}
          </h1>
        </div>

        <div className="flex items-center gap-2">
          {listing.capacity && (
            <div className="flex items-center gap-0.5">
              <svg
                className="w-3 h-3 text-gray-600"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
                role="img"
                width="1em"
                height="1em"
                preserveAspectRatio="xMidYMid meet"
                viewBox="0 0 36 36"
              >
                <path
                  fill="currentColor"
                  d="M12 16.14h-.87a8.67 8.67 0 0 0-6.43 2.52l-.24.28v8.28h4.08v-4.7l.55-.62l.25-.29a11 11 0 0 1 4.71-2.86A6.59 6.59 0 0 1 12 16.14Z"
                />
                <path
                  fill="currentColor"
                  d="M31.34 18.63a8.67 8.67 0 0 0-6.43-2.52a10.47 10.47 0 0 0-1.09.06a6.59 6.59 0 0 1-2 2.45a10.91 10.91 0 0 1 5 3l.25.28l.54.62v4.71h3.94v-8.32Z"
                />
                <path
                  fill="currentColor"
                  d="M11.1 14.19h.31a6.45 6.45 0 0 1 3.11-6.29a4.09 4.09 0 1 0-3.42 6.33Z"
                />
                <path
                  fill="currentColor"
                  d="M24.43 13.44a6.54 6.54 0 0 1 0 .69a4.09 4.09 0 0 0 .58.05h.19A4.09 4.09 0 1 0 21.47 8a6.53 6.53 0 0 1 2.96 5.44Z"
                />
                <circle cx="17.87" cy="13.45" r="4.47" fill="currentColor" />
                <path
                  fill="currentColor"
                  d="M18.11 20.3A9.69 9.69 0 0 0 11 23l-.25.28v6.33a1.57 1.57 0 0 0 1.6 1.54h11.49a1.57 1.57 0 0 0 1.6-1.54V23.3l-.24-.3a9.58 9.58 0 0 0-7.09-2.7Z"
                />
                <path fill="none" d="M0 0h36v36H0z" />
              </svg>
              <span className="text-sm">{listing.capacity} Guests</span>
            </div>
          )}

          {listing.rooms && (
            <div className="flex items-center gap-0.5">
              <svg
                className="w-3 h-3 text-gray-600"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
                role="img"
                width="1em"
                height="1em"
                preserveAspectRatio="xMidYMid meet"
                viewBox="0 0 24 24"
              >
                <path
                  fill="currentColor"
                  d="M5 5v14a1 1 0 0 0 1 1h3v-2H7V6h2V4H6a1 1 0 0 0-1 1zm14.242-.97l-8-2A1 1 0 0 0 10 3v18a.998.998 0 0 0 1.242.97l8-2A1 1 0 0 0 20 19V5a1 1 0 0 0-.758-.97zM15 12.188a1.001 1.001 0 0 1-2 0v-.377a1 1 0 1 1 2 .001v.376z"
                />
              </svg>

              <span className="text-sm">{listing.rooms} rm</span>
            </div>
          )}
        </div>

        <div className="flex gap-1 justify-center items-center mt-2">
          <Button
            onClick={() => {
              router.push({
                query: {
                  ...router.query,
                  index: index,
                },
              });
            }}
            className="!rounded-lg mt-2 h-[40px] !flex gap-1 !px-4 items-center justify-center w-full btn-gradient"
          >
            <span className="text-white font-bold text-sm">
              check availability
            </span>
          </Button>

          <PopoverBox
            panelClassName="bg-white absolute rounded-xl shadow-md mt-1 border -left-[20px] w-[250px] p-1"
            btnPopover={
              <div className="!rounded-lg cursor-pointer mt-2 !w-[60px] !h-[40px] !flex !px-0 !py-0 items-center justify-center bg-gray-200 hover:bg-gray-300 transition-colors duration-300">
                <Icon
                  className="w-8 h-8"
                  icon="carbon:overflow-menu-horizontal"
                />
              </div>
            }
          >
            <Link href={`/partner/lodges/${listing.slug}/actions`}>
              <a>
                <div className="py-2 px-2 cursor-pointer hover:bg-gray-100 rounded-md text-sm transition-colors duration-300">
                  Add/edit availability
                </div>
              </a>
            </Link>

            <div className="py-2 px-2 cursor-pointer hover:bg-gray-100 rounded-md text-sm transition-colors duration-300">
              View your accommodation
            </div>

            <div className="py-2 px-2 cursor-pointer hover:bg-gray-100 rounded-md text-sm transition-colors duration-300">
              Request for a change
            </div>

            <div className="py-2 px-2 text-red-500 cursor-pointer hover:bg-gray-100 rounded-md text-sm transition-colors duration-300">
              Request to delete accommodation
            </div>
          </PopoverBox>
        </div>
      </div>
    </div>
  );
}

Accommodation.propTypes = {};

export default Accommodation;
