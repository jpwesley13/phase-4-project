import { useFormik } from "formik";
import { useState, useEffect } from "react";
import * as yup from "yup";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context and hooks/AuthContext";

function Signup() {

    const [biomes, setBiomes] = useState([]);
    const { setTrainer } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        fetch('/biomes')
        .then(res => res.json())
        .then(data => setBiomes(data))
        .catch(error => console.error(error));
    }, []);

    const formSchema = yup.object().shape({
        name: yup.string().required("Must enter name.").max(24),
        age: yup.number().integer().required("Must enter age.").typeError("Please enter an Integer").min(10, "Must be at least 10 years old to join."),
        image: yup.string().optional(),
        biome_id: yup.string().required(`If you have no preference, select "No Preference"`),
        password: yup.string().min(6, "Password must be at least 6 characters.").max(30, "Password cannot exceed 30 characters.").required("Must create a password."),
        confirmPassword: yup.string().oneOf([yup.ref('password'), null], "Passwords must match.").required("Required.")
    });

    const onSubmit = async (values, actions) => {
        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(values),
        })
        .then(async res => {
            const data = await res.json();
            if (res.status >= 400) {
                actions.setErrors(data.errors);
            } else {
                setTrainer(data);
                navigate('/');
                actions.resetForm();
            }
        })
        .catch(error => console.error(error))
      };
    
    const {values, handleBlur, handleChange, handleSubmit, touched, errors, isSubmitting} = useFormik({
        initialValues: {
            name: "",
            age: "",
            image: "",
            biome_id: "",
            password: "",
            confirmPassword: ""
        },
        validationSchema: formSchema,
        onSubmit,
    });

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="name">Name</label>
            <input
                value={values.name}
                onChange={handleChange}
                onBlur={handleBlur}
                id="name" 
                type="name" 
                placeholder="Enter your name"
                className={errors.name && touched.name ? "input-error" : ""} 
            />
            {errors.name && touched.name && <p className="error">{errors.name}</p>}
            <label htmlFor="age">Age</label>
            <input
                value={values.age}
                onChange={handleChange}
                onBlur={handleBlur}
                id="age" 
                type="number" 
                placeholder="Enter your age" 
                className={errors.age && touched.age ? "input-error" : ""} 
            />
            {errors.age && touched.age && <p className="error">{errors.age}</p>}
            <label htmlFor="password">Password</label>
            <input
                value={values.password}
                onChange={handleChange}
                onBlur={handleBlur}
                id="password" 
                type="password" 
                placeholder="Enter your password"
                className={errors.password && touched.password ? "input-error" : ""} 
            />
            {errors.password && touched.password && <p className="error">{errors.password}</p>}
            <label htmlFor="password">Confirm Password</label>
            <input
                value={values.confirmPassword}
                onChange={handleChange}
                onBlur={handleBlur}
                id="confirmPassword" 
                type="password" 
                placeholder="Confirm your password"
                className={errors.confirmPassword && touched.confirmPassword ? "input-error" : ""} 
            />
            {errors.confirmPassword && touched.confirmPassword && <p className="error">{errors.confirmPassword}</p>}
            <label htmlFor="image">Profile Picture</label>
            <input
                value={values.image}
                onChange={handleChange}
                onBlur={handleBlur}
                id="image" 
                type="text" 
                placeholder="Post your profile picture's url" 
                className={errors.image && touched.image ? "input-error" : ""} 
            />
            {errors.image && touched.image && <p className="error">{errors.image}</p>}
            <label htmlFor="biome">Favorite Biome</label>
            <select
                value={values.biome_id}
                onChange={handleChange}
                onBlur={handleBlur}
                id="biome_id" 
                type="text" 
                placeholder="Select your favorite biome" 
                className={errors.biome_id && touched.biome_id ? "input-error" : ""}>
                    <option value="" hidden disabled>Select a biome</option>
                    {biomes.map((biome) => (
                    <option key={biome.id} value={biome.id}>{biome.name}</option>
                ))}
            </select>
            {errors.biome_id && touched.biome_id && <p className="error">{errors.biome_id}</p>}
                <button disabled={isSubmitting} type="submit">Submit</button>
        </form>
    )
};
export default Signup;