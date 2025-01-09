# A few notes 📝

## To start 🚀 
``` bash
cd frontend
```
``` bash
npm start
```

## What you will currently see 👀
`ListComponents.js` is currently the landing screen, this displays the current components that are built out for the front end

## Important note ⚠️
Please do not build straight into the `main` branch
Have the reviewer review and merge the code

### Keeping Text and colors modular and consistent
#### Text 
All text variables are defines in `variables.css` and is set in `index.css`. So if you are setting className to texts, please use the appropriate className set in `index.css`. These are consistent with the Figma names, so refer to that if you are uncertain.

Here is an example 
`UserInfo.js`
```javascript
<div className="text-container">
  <div className="headline-small">{userName}</div>
  <div className="body-medium">{userEmail}</div>
</div>
```

`Index.css`
```css
.headline-small {
  font-size: var(--headline-small-size);
}

.body-medium {
  font-size: var(--body-medium-size);
  font-weight: var(--body-medium-weight);
}
```

#### Color
All colors are defined in `variables.css`. Please use these in css files 
Here is an example 
`Buttons.css`
```css
.btn-primary-color {
    background-color: var(--primary);
    color: var(--onPrimary);
}

.btn-secondary-color {
background-color: var(--secondary);
color: var(--onSecondary);
}
```
## How to contribute 🤝
  1. `git pull` on the main branch
  2. Create a new branch using the name of the component you are building our. Add feat at the start ex `feat/component-name`
  3. build the component, make sure to build it in a way that the component can be used throughout the application. So use input params and do not hard code the values in the component itself
  4. Add the component to the ListComponent.js to show how it can be used
  5. Commit the changes and push the branch
  6. Create a pull request and add Jo as the reviewer

# Figma design prototype 🎨
Refer to this for design references

https://www.figma.com/design/23paUag3OLf5j3fJrYZzb6/Front-End-Design?node-id=0-1&t=SbOOUuTE0FTGAmQ1-1

# Components used
  - Multi Select drop down :
    - https://www.npmjs.com/package/multiselect-react-dropdown  
