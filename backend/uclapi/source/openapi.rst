OpenAPI
=================

We maintain our public-facing documentation and SDKs using an OpenAPI 3 (Swagger) specification. This page describes
the process you might take to update the specification when you make a change to the API interface.

The OpenAPI specification is tied to each deployment, so the frontend documentation is always in sync with the latest deployment.

See the `uclapi.openapi.json <https://github.com/uclapi/uclapi/blob/master/uclapi.openapi.json>`_ file in the root of the repository.


Contents
-------------------------
.. toctree::
   openapi

Viewing the specification
----------------------------

`Swagger Editor <https://editor.swagger.io/>`_ is a free online OpenAPI specification editor and viewer which can be
used to edit/render specifications (in JSON or YAML format).

Alternatively, the latest version of the specification will always be available at `the UCL API docs site <http://docs.uclapi.com/>`_.

Understanding the specification
--------------------------------

You don't need to be an OpenAPI expert to understand the specification -- the `official docs <https://swagger.io/docs/specification/about/>`_
are a good starting point, but a brief overview of the standard and how we're using it is below:

* Use `Tags <https://swagger.io/docs/specification/grouping-operations-with-tags/>`_ to group endpoints by their category (e.g., ``workspaces``, ``analytics``, etc.)
* Parameters are defined in the `components.parameters <https://swagger.io/docs/specification/components/>`_ section
* Response schemas are defined in the ``components.schemas`` section
* Example errors are defined in the ``components.examples`` section
* Each endpoint is defined as a `path <https://swagger.io/docs/specification/paths-and-operations/>`_

   Note: OpenAPI currently requires us to explicitly add all the different possible errors to each path individually - there's no way to set these globally yet.

Updating the specification
----------------------------

Whilst Swagger Editor could be used to update the specification, you can use `Insomnia Designer <https://insomnia.rest/products/designer/>`_,
which allows you to design, preview, lint and debug OpenAPI specifications in its own editor.

It's usually easier to just make the changes manually inside one of these editors, rather than using something like Swagger Inspector because it's harder to integrate that tool into an existing OpenAPI API specification.

Automatic code generation
----------------------------

We use the `OpenAPI Generator project <https://openapi-generator.tech/>`_ to automatically generate SDKs for public use.

At the moment we only have a `JavaScript SDK <https://github.com/uclapi/uclapi-js-sdk>`_ being automatically generated
and published to npm.

The idea is to create more repos that simply use the specification to automatically generate SDKs in different languages
to simplify the development experience for developers wanting to use UCL API.
