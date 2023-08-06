# dlsproc
> Download Spanish procurement


One is better off checking the wiki, but this is Python code meant to download Spanish government's [Plataforma de contratación del sector público](https://contrataciondelestado.es) *metadata* (right now, it does **not** download any document). Data can be accessed through [Ministerio de Hacienda y Función Pública](https://www.hacienda.gob.es/es-ES/GobiernoAbierto/Datos%20Abiertos/Paginas/licitaciones_plataforma_contratacion.aspx).

## Install

`pip install dlsproc`

## How to use

The software can be exploited as a library or as *standalone* scripts. 

### Scripts

For testing purposes one can download *Outsiders contracts for 2018*, either directly by clicking [this link](https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_1044/PlataformasAgregadasSinMenores_2018.zip) or, if [wget](https://www.gnu.org/software/wget/) is available`, running
```
wget https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_1044/PlataformasAgregadasSinMenores_2018.zip
```

#### Processing zip files

Running
```
dlsproc_process_zip.py PlataformasAgregadasSinMenores_2018.zip 2018.parquet
```
outputs the file `2018.parquet` (the name being given by the 2nd argument), which contains a `pd.DataFrame` with all the 2018 metadata. It can be readily loaded (in Python, through [Pandas](https://pandas.pydata.org/)' `pd.read_parquet`). The columns of the `pd.DataFrame` stored inside are *multiindexed* (meaning one could get columns such as `(ContractFolderStatus','ContractFolderID)` and `(ContractFolderStatus','ContractFolderStatusCode)`.  This is very convenient when visualizing the data (see the [the documentation for the `hier`module](https://manuvazquez.github.io/dlsproc/hierarchical.html#flat_df_to_multiindexed_df)).

#### From hierarchical (*multiindexed*) columns to plain ones

The columns of the above `pd.DataFrame` can be *flattened* to get, in the example above, `ContractFolderStatus - ContractFolderID` and `ContractFolderStatus - ContractFolderStatusCode`, respectively. Additionally, some renaming might be applied following the mapping in some YAML file
```
dlsproc_rename_cols.py 2018.parquet samples/PLACE.yaml 2018_flattened.parquet
```

This would yield a `pd.DataFrame` with *plain* columns in file `2018_flattened.parquet`. Renaming is carried out using the mapping in [PLACE.yaml](samples/PLACE.yaml), which can be found in the `samples` directory of this repository.

#### Appending new data to an existing (column-*multiindexed*) *parquet* file

We can append new data to an existing `pd.DataFrame`. Let us, for instance, download, [data from January 2022](https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_1044/PlataformasAgregadasSinMenores_202201.zip),
```
wget https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_1044/PlataformasAgregadasSinMenores_202201.zip
```
and extends the existing [parquet](https://parquet.apache.org/) file with data extracted from the newly downloaded *zip* file,
```
dlsproc_extend_parquet_with_zip.py 2018.parquet PlataformasAgregadasSinMenores_202201.zip 2018_202201.parquet
```
The *combined* data was saved in `2018_202201.parquet`.
