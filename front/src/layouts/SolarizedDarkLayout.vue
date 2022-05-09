<template>
  <!--
        WARNING:
            Anything you put in this component will be seen in any of the subcomponents
            The only purpose of this component is to display anything under the /Anson/ address
            There are times you would want something else in this component
            For example, you might want to have a toolbar available on all of your pages
            Or you might want to have a thing that pulls out from the sides (a drawer)
            Those would go here and then be seen on any of the pages underneath /Anson/
  -->
  <div class="customer-layout-top-css">
    <!--
        thing put here will be on top of the page
    -->
    <router-view/>
    <!--
        thing put here will be at the bottom of the page
    -->
  </div>
</template>

<script>
export default {};
</script>

<style>
/*
    Any styles you put in here will be propagated down to all of your other pages
    For an example, you can take a look at NathanLayout.vue
*/
.customer-layout-top-css {
  background-color: #002b36;
  color: #93a1a1;
  padding: 3% 5% 10% 5%;
  min-height: 100vh;
}
</style>
