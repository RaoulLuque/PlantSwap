# Test execution

As discussed in [testing_framework_and_assertion_library.md](../milestone_2/testing_framework_and_assertion_library) and  [continuous_integration.md](../milestone_2/continuous_integration.md) from the documentation of milestone 2, we have an automatic testing system in place that tests the codebase on every push to the repository. These runs can be seen in the [actions tab](https://github.com/RaoulLuque/PlantSwap/actions) of the [repository](https://github.com/RaoulLuque/PlantSwap). As can be seen there as well as in the main README of the repository - see [visualization_of_continuous_integration.md](../milestone_2/visualization_of_continuous_integration.md) - the tests execute successfully on reliable basis.

Furthermore, it can be said that the code base is not only being tested successfully but also thoroughly. So far there are 68 tests that cover all existing API endpoints covering all possible exceptions that might occur therefore achieving a coverage of 100%. We want to demonstrate the design of the tests for a specific endpoints in the following. 

Consider the following delete plant API endpoint or rather how it looks in our codebase (found in [plants.py](../../app/api/routers/plants.py)).

```python
@router.post("/plants/{id}", response_model=PlantPublic)
def delete_plant(
    session: SessionDep, current_user: CurrentUserDep, id: uuid.UUID
) -> Any:
    """
    Delete plant with given id if current_user is owner.
    :param current_user: Currently logged-in user
    :param id: id of plant to be deleted.
    :param session: Current database session.
    :return: Plant with given id, if deleted successfully.
    """
    plant = session.get(Plant, id)
    if plant is None:
        raise HTTPException(
            status_code=404,
            detail="No plant with the given id exists.",
        )
    if not current_user.is_superuser:
        if plant.owner_id != current_user.id:
            raise HTTPException(
                status_code=401,
                detail="You are not the owner of the plant.",
            )
    plant = plants_crud.delete_plant_ad(session, plant)
    return plant
```
As one can see, there are 2 possible exceptions that might occur. Either the provided plant (id) does not exist or the user is not the owner of the plant. In this case an exception will be thrown that the user is not the owner of the plant (the fact that user might this way guess plant ids is not a privacy concern since these are publicly visible/readable from other endpoints and cannot be used in a malicious way). Actually however, there is another exception that might occur if the user is not authenticated at all. In that case `CurrentUserDep` will throw a corresponding exception. Therefore, the tests for this endpoint are the following:

- test_delete_plant_not_found
- test_delete_plant_user_not_authorized
- test_delete_plant_not_authenticated
- test_delete_plant_user_success
- test_delete_plant_superuser_success

These tests are found in [test_plants.py](../../app/tests/api/routers/test_plants.py).
