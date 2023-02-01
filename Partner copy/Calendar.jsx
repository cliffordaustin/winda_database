import React, { useState } from "react";
import PropTypes from "prop-types";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import timeGridPlugin from "@fullcalendar/timegrid";
import listPlugin from "@fullcalendar/list";
import { createGlobalStyle } from "styled-components";
import "react-day-picker/dist/style.css";
import "react-big-calendar/lib/css/react-big-calendar.css";

import { Calendar as BigCalendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";

const localizer = momentLocalizer(moment);

function Calendar() {
  const GlobalStyle = createGlobalStyle`
  .rdp-cell {
    min-width: 20px !important;
    min-height: 20px !important;
  }
  .rdp-button {
    border-radius: 100px !important;
    font-size: 0.8rem !important;
  }
  .rdp-months {
    width: 100% !important;
  }
  .rdp-day_range_middle {
    opacity: 0.5 !important;
  }
`;

  const resources = [
    {
      id: "a",
      title: "Room A",
    },
    {
      id: "b",
      title: "Room B",
    },
    {
      id: "c",
      title: "Room C",
    },
  ];

  return (
    <>
      <GlobalStyle></GlobalStyle>

      <div className="hidden md:block">
        {/* <FullCalendar
          plugins={[timeGridPlugin]}
          initialView="timeGridDay"
          eventClassNames={
            "cursor-pointer !border-l-[6px] !border-t-[0px] !border-r-[0px] !border-b-[0px]"
          }
          editable={true}
          selectable={true}
          selectMirror={true}
          dayHeaderContent={(args) => {
            return args.date.toLocaleString("en-US", {
              weekday: "short",
            });
          }}
          headerToolbar={{
            right: "prev,next",
          }}
        /> */}

        <BigCalendar
          localizer={localizer}
          resources={resources}
          events={[
            {
              id: 1,
              title: "John Doe",
              start: moment().toDate(),
              end: moment().add(330, "minutes").toDate(),
              allDay: false,
              resourceId: "a",
            },
            {
              id: 1,
              title: "Jane Doe",
              start: moment().toDate(),
              end: moment().add(530, "minutes").toDate(),
              allDay: false,
              resourceId: "b",
            },
          ]}
          views={["day", "week", "month"]}
          startAccessor="start"
          endAccessor="end"
          style={{ height: 600 }}
        />
      </div>
    </>
  );
}

Calendar.propTypes = {};

export default Calendar;
