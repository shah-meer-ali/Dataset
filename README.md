# Dataset

Electronics prognostics / accelerated aging dataset covering:

- `12.+Capacitor+Electrical+Stress/` — capacitor electrical stress aging data
- `13.+MOSFET+Thermal+Overstress+Aging/` — MOSFET thermal overstress aging data
- `8.+IGBT+Accelerated+Aging/` — IGBT accelerated aging data

## Large files

GitHub blocks files over 100MB in a normal repository, so 50 files (mostly
`.mat` measurement files and two `.zip` archives, totaling ~13GB) are **not**
stored in this repo. They're attached instead to the
[`v1-large-files` release](https://github.com/shah-meer-ali/Dataset/releases/tag/v1-large-files).

This includes:
- `ES10.mat`, `ES12.mat`, `ES14.mat` — large capacitor stress files (belong in
  `12.+Capacitor+Electrical+Stress/12. Capacitor Electrical Stress/`)
- 45 `Test_*.mat` files — belong in
  `13.+MOSFET+Thermal+Overstress+Aging/13. MOSFET Thermal Overstress Aging/MOSFET_Thermal_Overstress_Aging_v0/MOSFET_Thermal_Overstress_Aging_v0/`
- `IGBTAgingData_04022009.zip` — belongs in
  `8.+IGBT+Accelerated+Aging/8. IGBT Accelerated Aging/`
- `MOSFET_Thermal_Overstress_Aging_v0.zip.00.part` through `.03.part` — a
  7.3GB zip archive (`MOSFET_Thermal_Overstress_Aging_v0.zip`, containing the
  same MOSFET test data as the `Test_*.mat` files above, kept for
  completeness) split into 4 parts because it exceeds the 2GB GitHub Release
  asset limit. Belongs in
  `13.+MOSFET+Thermal+Overstress+Aging/13. MOSFET Thermal Overstress Aging/`.

### Rejoining the split zip

After downloading all 4 `.part` files into the same folder:

**Linux / macOS:**
```bash
cat MOSFET_Thermal_Overstress_Aging_v0.zip.*.part > MOSFET_Thermal_Overstress_Aging_v0.zip
```

**Windows (Command Prompt):**
```cmd
copy /b MOSFET_Thermal_Overstress_Aging_v0.zip.00.part+MOSFET_Thermal_Overstress_Aging_v0.zip.01.part+MOSFET_Thermal_Overstress_Aging_v0.zip.02.part+MOSFET_Thermal_Overstress_Aging_v0.zip.03.part MOSFET_Thermal_Overstress_Aging_v0.zip
```

**Windows (PowerShell):**
```powershell
Get-Content MOSFET_Thermal_Overstress_Aging_v0.zip.*.part -Raw -AsByteStream | Set-Content MOSFET_Thermal_Overstress_Aging_v0.zip -AsByteStream
```
