# GASSgraphql

```
docker pull paulgass/2020:pmggql
```
```
mutation{
  createCandidate(input:{
    brandiId: 230923,
    firstName: "Party",
    lastName: "Door",
    phoneNumber: "313-555-4432",
    homeOfRecord: "Toronto",
    sex: Male,
    middleInitial: "N",
    socialSecurityNumber: "777-98-2345",
    dob: "2000-01-02",
    arrivedFrom: "TheSix",
    arrivalDate: "2001-01-01T23:23:23"
  }) {
    candidate{
      id
      firstName
      lastName
      phoneNumber
      homeOfRecord
      sex
      middleInitial
      socialSecurityNumber
      dob
      arrivedFrom
      brandiId
    }
  }
}
```
