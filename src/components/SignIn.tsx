import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBInput,
} from "mdb-react-ui-kit";
import "./SignIn.css";
import { useState, useContext } from "react";
import AuthContext from "../contexts/AuthProvider";
// import { useCookies } from "react-cookie";

const SignIn = () => {
  const { loggedIn, setLoggedIn } = useContext(AuthContext);
  // const [cookies, setCookie, removeCookie] = useCookies(["auth"]);
  const [inputEmail, setInputEmail] = useState("");
  const [inputPassword, setInputPassword] = useState("");
  // cookies["auth"] = auth;
  const handleSubmit = async () => {
    console.log("handleSubmit...");
    // make login api call to "44.201.213.82:8000/login"
    const response = await fetch("http://44.201.213.82:8000/login", {
      method: "POST",
      body: JSON.stringify({ username: inputEmail, password: inputPassword }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        console.log(data);
        if (data.result === "success") {
          setLoggedIn(true);
        } else {
          setLoggedIn(false);
        }
      })
      .then(() => {
        console.log(loggedIn);
      });
  };

  return (
    <MDBContainer fluid>
      <MDBRow className="d-flex justify-content-center align-items-center h-100">
        <MDBCol col="12">
          <MDBCard
            className="bg-dark text-white my-5 mx-auto"
            style={{ borderRadius: "1rem", maxWidth: "400px" }}
          >
            <MDBCardBody className="p-5 d-flex flex-column align-items-center mx-auto w-100">
              <h2 className="fw-bold mb-2 text-uppercase">Login</h2>
              <p className="text-white-50 mb-5">
                Please enter your login and password!!
              </p>
              <MDBInput
                wrapperClass="mb-4 mx-5 w-100"
                labelClass="text-white"
                label="Email address"
                id="formControlLg"
                type="email"
                size="lg"
                value={inputEmail}
                onChange={(e) => setInputEmail(e.target.value)}
              ></MDBInput>
              <MDBInput
                wrapperClass="mb-4 mx-5 w-100"
                labelClass="text-white"
                label="Password"
                id="formControlLg2"
                type="password"
                size="lg"
                value={inputPassword}
                onChange={(e) => setInputPassword(e.target.value)}
              ></MDBInput>

              <button
                type="button"
                className="btn btn-outline-light"
                onClick={handleSubmit}
              >
                Sign in
              </button>
            </MDBCardBody>
          </MDBCard>
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
};

export default SignIn;
