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

I use [ilovepdf](https://www.ilovepdf.com/pdf_to_excel) to convert the course list (pdf) to an Excel file.

Then run a script to convert the Excel file to JSON.
```sh
pnpm generate-data
```

## Features

- [X] Download calendar as an `.ics` file.
- [X] Separate lecture and exam schedules
- [ ] Support mid-sem/end-sem system.
- [ ] View schedule as a table
- [ ] Store and retrieve your course selection using cookies.
- [ ] Templates based on recommendation made by Institute (First five semester)
