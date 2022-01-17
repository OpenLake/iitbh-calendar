# IITBh Calendar Generator

Select your courses and generate a `.ics` 📆 calendar file.

https://supercoww.github.io/iitbh-calendar/

## Development

- Get [pnpm](https://pnpm.io)
- Install dependencies
  ```sh
  pnpm install
  ```
- Run
  ```sh
  pnpm dev
  ```

## Course List

I use [ilovepdf](https://www.ilovepdf.com/pdf_to_excel) to convert the course list to an Excel file.

Then run a script to convert the Excel file to JSON.
```sh
pnpm generate-data
```
