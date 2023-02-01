import React, { Fragment, useState } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { Icon } from "@iconify/react";
import { useRouter } from "next/router";

export default function SelectOptions({ options }) {
  const [selected, setSelected] = useState(options[0]);

  const router = useRouter();

  return (
    <Listbox value={selected} onChange={setSelected}>
      <div className="relative mt-1">
        <Listbox.Button className="relative w-full bg-white cursor-default rounded-sm py-3 border pl-3 pr-10 text-left shadow-md focus:outline-none text-sm">
          <span className="block truncate">{selected.name}</span>
          <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
            <Icon
              className="h-5 w-5 text-gray-400"
              icon="majesticons:chevron-down-line"
            />
          </span>
        </Listbox.Button>
        <Transition
          as={Fragment}
          leave="transition ease-in duration-100"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <Listbox.Options className="absolute mt-1 z-20 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
            {options.map((person, personIdx) => (
              <Listbox.Option
                key={personIdx}
                className={({ active }) =>
                  `relative cursor-default select-none py-2 pl-10 pr-4 ${
                    active ? "bg-blue-100 text-blue-900" : "text-gray-900"
                  }`
                }
                value={person}
                onClick={() => {
                  router.replace(
                    {
                      query: {
                        ...router.query,
                        option:
                          person.value === "Analytics"
                            ? 3
                            : person.value === "Bookings"
                            ? 2
                            : 1,
                      },
                    },
                    undefined,
                    { shallow: true }
                  );
                }}
              >
                {({ selected }) => (
                  <>
                    <span
                      className={`block text-sm truncate ${
                        selected ? "font-medium" : "font-normal"
                      }`}
                    >
                      {person.name}
                    </span>
                    {selected ? (
                      <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-blue-600">
                        <Icon
                          className="h-5 w-5"
                          icon="material-symbols:check-small-rounded"
                        />
                      </span>
                    ) : null}
                  </>
                )}
              </Listbox.Option>
            ))}
          </Listbox.Options>
        </Transition>
      </div>
    </Listbox>
  );
}
