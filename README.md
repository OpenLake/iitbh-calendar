# IITBh Calendar Generator

Easily generate your course timetable as a `.ics` 📆 file.

Visit https://openlake.github.io/iitbh-calendar/ to use.

## Setup for development

- Install node and get [pnpm](https://pnpm.io)
- Install dependencies
  ```sh
  pnpm install
  ```
- Run development server
  ```sh
  pnpm dev
  ```
- These commands will run development server on port 3000.

## Deploying

- Use `deploy.sh` script to deploy

```
usage: ./deploy.sh -u <USERNAME> [-r <REPO>] [-d <DOMAIN>] [-h] [-y]
         -d Custom domain name
         -h Display help
         -r GitHub repo name
         -u GitHub username [Required]
         -v Be verbose
         -y Do not ask confirmation
```

## Course List

Convert the pdf to excel using website like [ilovepdf](https://www.ilovepdf.com/pdf_to_excel)
Verify that the order of the fields in data/generateJson.js and your excel file is same, if not, update either of the file.

Then run a script to convert the Excel file to JSON.

```sh
pnpm generate-data
```

It will try to resolve course slots automatically and give you a list of
courses which needs to be edited manually.

## Features

- [x] Download calendar as an `.ics` file.
- [x] Separate lecture and exam schedules
- [x] Support mid-sem/end-sem system.
- [x] View schedule as a table
- [ ] Store and retrieve your course selection using cookies.
- [x] Templates based on recommendation made by Institute (First five semester)
