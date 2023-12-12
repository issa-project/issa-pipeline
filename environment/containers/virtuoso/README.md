## Virtuoso Engine Advanced Configuration

### Enable Faceted Browsing

By enabling Faceted Browsing, you will be able to use /describe endpoint to get a description of a resource in the Knowledge Graph. The description will include the values of the resource's properties. T

>:point_right: This feature is not enabled by default in the Virtuoso container version that is tested in ISSA. More details can be found in the [Virtuoso documentation](https://vos.openlinksw.com/owiki/wiki/VOS/VirtFacetBrowserInstallConfig).

To enable Faceted Browser in Virtuoso, you need to follow these steps:

1. Open the Virtuoso Conductor web interface http://localhost:8890/conductor.
2. Login with the credentials `dba` and the password that you have set during the Virtuoso installation.
2. Navigate to the `System Admin/Packages` tab.
3. Check `fct` package and click the `Install/Upgrade` button.
4. Restart the Virtuoso container.

>:point_right: Optionally run the ISQL commands suggested in the [Virtuoso documentation](https://vos.openlinksw.com/owiki/wiki/VOS/VirtFacetBrowserInstallConfig) to speed up the Faceted Browser tasks.

### Enable Cross-Origin Resource Sharing (CORS) for SPARQL endpoint

CORS enables web applications to access resources from different domains.

To enable CORS for SPARQL endpoint, you need to follow these steps:

1. Open the Virtuoso Conductor web interface http://localhost:8890/conductor.
2. Login with the credentials `dba` and the password that you have set during the Virtuoso installation.
2. Navigate to the `Web Application Server/Virtual Domains and Directories` tab.
3. Locate the `/sparql` logical Path and click on the `Edit` button.
4. Enter `*` in the `Cross-Origin Resource Sharing` input field. Optionally you can check the Reject Unintended CORS check-box.
5. Click on the `Save Changes` button.
7. Restart the Virtuoso container.

More details can be found in the [Virtuoso documentation](https://vos.openlinksw.com/owiki/wiki/VOS/VirtTipsAndTricksCORsEnableSPARQLURLs).


>:point_right: If HTTPS is enabled for the Virtuoso container, you need to enable CORS for the HTTPS SPARQL endpoint as well.
