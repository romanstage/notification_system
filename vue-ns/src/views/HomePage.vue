<template>
    <v-row justify="center">
        <Home></Home>
        <div class="col-3">
            <CaledarReports></CaledarReports>
        </div>
    </v-row>

</template>

<script>
    import CaledarReports from "../components/CaledarReports";
    import Home from "../components/Home";

    export default {
        name: "HomePage",
        components: {Home, CaledarReports}
    }
</script>

<style scoped>

</style>