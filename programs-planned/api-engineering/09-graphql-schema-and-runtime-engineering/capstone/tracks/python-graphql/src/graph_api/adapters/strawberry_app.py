"""Optional Strawberry adapter.

This file is excluded from the dependency-light proof. Install the `server`
extra and use the course schema/resolver policies before running it.
"""

def create_app():
    import strawberry
    from fastapi import FastAPI
    from strawberry.fastapi import GraphQLRouter

    @strawberry.type
    class Viewer:
        subject: strawberry.ID
        tenant_id: strawberry.ID

    @strawberry.type
    class Query:
        @strawberry.field
        def viewer(self, info: strawberry.Info) -> Viewer:
            principal = info.context["principal"]
            return Viewer(subject=principal.subject, tenant_id=principal.tenant_id)

    schema = strawberry.Schema(query=Query)
    app = FastAPI()
    app.include_router(GraphQLRouter(schema), prefix="/graphql")
    return app
